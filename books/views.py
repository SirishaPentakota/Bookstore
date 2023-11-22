from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from .import models
from django.db.models import Q
import os

from django.http import FileResponse
from .forms import BookForm
from .forms import BookSearchForm
from .models import UserProfile,Book 
from .models import KannadaBook,SELFHELP_BOOK,CHILDREN

from django.views.decorators.csrf import csrf_exempt



# Create your views here.

def home(request):
    return render(request,'index.html')
def all_categories(request):
    
    return render(request, 'allcategories.html')

def kannada_books(request):
    kannada_books = KannadaBook.objects.all()
    
    if request.user.is_authenticated:
        user_saved_titles = request.user.userprofile.saved_books.values_list('title', flat=True)
    else:
        user_saved_titles = []

    context = {
        'kannada_books': kannada_books,
        'user_saved_titles': user_saved_titles,
    }

    return render(request, 'kannada_books.html', context)
def selfhelp_books(request):
    self_help_books = SELFHELP_BOOK.objects.all()
    
    if request.user.is_authenticated:
        user_saved_titles = request.user.userprofile.saved_books.values_list('title', flat=True)
    else:
        user_saved_titles = []

    context = {
        'selfhelp_book': self_help_books,
        'user_saved_titles': user_saved_titles,
    }

    return render(request, 'selfhelp_books.html', context)

    
def children(request):
    children_books = CHILDREN.objects.all()
    
    if request.user.is_authenticated:
        user_saved_titles = request.user.userprofile.saved_books.values_list('title', flat=True)
    else:
        user_saved_titles = []

    context = {
        'children_books': children_books,
        'user_saved_titles': user_saved_titles,
    }

    return render(request, 'children_books.html', context)

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the username or email already exists
        if User.objects.filter(username=username).exists():
            error_message = 'Username already registered. Please choose a different username.'
        elif User.objects.filter(email=email).exists():
            error_message = 'Email already registered. Please use a different email.'
        else:
            # Create the user if not already registered
            user = User.objects.create_user(username=username, email=email, password=password)
            # You can also log the user in here if desired
            return redirect('login')  # Redirect to login page after successful registration
        
        return render(request, 'register.html', {'error_message': error_message})

    return render(request, 'register.html')
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the home page after successful login
        else:
            messages.error(request, 'Invalid username or password')  # Display error message

    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    
    return redirect('home')

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Replace 'book_list' with the URL name for the list view of all books
    else:
        form = BookForm()
    
    return render(request, 'add_book.html', {'form': form})


def book_list(request):
    books = Book.objects.all()  # Retrieve all books
    selfhelp_book = SELFHELP_BOOK.objects.all()
    kannada_books = KannadaBook.objects.all()
    children_books = CHILDREN.objects.all()
    return render(request, 'books.html', {'books': books, 'kannada_books': kannada_books, 'selfhelp_book': selfhelp_book,'children_books':children_books})

def book_search_view(request):
    form = BookSearchForm(request.GET)

    if form.is_valid():
        query = form.cleaned_data['query']

        print("Search Query:", query)

        # Filter books based on the search query in titles and authors using Q objects
        book_results = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )

        # Combine the results from the "all_books" category
        results = list(book_results)

        print("Results:", results)
    else:
        # If the form is not valid, show all books as the default result
        results = Book.objects.all()

    return render(request, 'books.html', {'form': form, 'books': results})


@login_required
def save_book(request, book_title):
    if request.user.is_authenticated:
        try:
            # Get the first book with the specified title
            book = Book.objects.filter(title=book_title).first()
            if book:
                user_profile, created = UserProfile.objects.get_or_create(user=request.user)
                user_profile.saved_books.add(book)

                # Display a success message
                messages.success(request, f'Book "{book.title}" added to your saved books.')

                # Render the books.html template with the updated context
                books = Book.objects.all()
                kannada_books = KannadaBook.objects.all()
                selfhelp_books = SELFHELP_BOOK.objects.all()
                children_books = CHILDREN.objects.all()
                context = {
                    'books': books,
                    'kannada_books': kannada_books,
                    'selfhelp_books': selfhelp_books,
                    'children_books': children_books,
                }
                return render(request, 'books.html', context)
            else:
                # Handle the case where no book with the given title is found
                return HttpResponseNotFound("Book not found.")
        except Book.MultipleObjectsReturned:
            # Handle the case where multiple books with the given title are found
            return HttpResponse("Multiple books found with the same title. Please contact support.")
    # Handle authentication or other error cases
    return redirect('books')

@login_required
def save_children_book(request, book_title):
    children_book = get_object_or_404(CHILDREN, title=book_title)

    # Create or get the corresponding Book instance
    book, created = Book.objects.get_or_create(
        title=children_book.title,
        author=children_book.author,
        pdf=children_book.pdf,
        cover=children_book.cover,
        flipkart_url=children_book.flipkart_url,
        
        # Set the price to the value of children_book.price
        price=children_book.price,
    )

    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    user_profile.saved_books.add(book)  # Save the Book instance to the user's profile

    # Redirect back to the 'children' page
    return redirect(reverse('children'))

@login_required
def save_kannada_book(request, book_title):
    kannada_book = get_object_or_404(KannadaBook, title=book_title)

    # Create or get the corresponding Book instance
    book, created = Book.objects.get_or_create(
        title=kannada_book.title,
        author=kannada_book.author,
        pdf=kannada_book.pdf,
        cover=kannada_book.cover,
        flipkart_url=kannada_book.flipkart_url,
    )

    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    user_profile.saved_books.add(book)  # Save the Book instance to the user's profile
    
    # Redirect back to the 'children' page
    return redirect(reverse('kannada_books'))
@login_required
def save_selfhelp_book(request, book_title):
    selfhelp_book = get_object_or_404(SELFHELP_BOOK, title=book_title)

    # Create or get the corresponding Book instance
    book, created = Book.objects.get_or_create(
        title=selfhelp_book.title,
        author=selfhelp_book.author,
        pdf=selfhelp_book.pdf,
        cover=selfhelp_book.cover,
        flipkart_url=selfhelp_book.flipkart_url,
        price=selfhelp_book.price,
    )

    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    user_profile.saved_books.add(book)  # Save the Book instance to the user's profile

    # Redirect back to the 'selfhelp_books' page
    return redirect(reverse('selfhelp_books'))



@login_required
def dashboard(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    saved_books = user_profile.saved_books.all()
    return render(request, 'dashboard.html', {'saved_books': saved_books})
def remove_book(request, book_title):
    if request.user.is_authenticated:
        try:
            # Get the first book with the specified title
            book = Book.objects.filter(title=book_title).first()
            if book:
                request.user.userprofile.saved_books.remove(book)
                # Redirect to the dashboard or a success page
                return redirect('dashboard')
            else:
                # Handle the case where no book with the given title is found
                return HttpResponseNotFound("Book not found.")
        except Book.MultipleObjectsReturned:
            # Handle the case where multiple books with the given title are found
            return HttpResponse("Multiple books found with the same title. Please contact support.")
    # Handle authentication or other error cases
    return redirect('dashboard')  # Redirect to the dashboard in case of error


def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        
        if new_password == confirm_password:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            messages.success(request, 'New password created successfully.Please Login')
            return redirect('login') 
    return render(request, 'forgot_password.html')





def all_books(request, title):
    # Query the books based on the selected title
    books = Book.objects.filter(title__icontains=title)  # Case-insensitive search by title

    return render(request, 'books.html', {'title': title, 'books': books})