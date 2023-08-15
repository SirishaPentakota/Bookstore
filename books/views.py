from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
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

# Create your views here.

def home(request):
    return render(request,'index.html')


def register(request):
    
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        
        user=User.objects.create_user(username=username,email=email,password=password)
        user.save()
        return redirect('home')
    return render(request,'register.html')

def login_user(request):
    
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        
        user= authenticate(username=username,password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"You are now logged in as {username}")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
    user_form = AuthenticationForm()
    return render(request,"login.html", {"user_form":user_form})

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
    books = Book.objects.all()
    return render(request, 'books.html', {'books': books})


def book_search_view(request):
    form = BookSearchForm(request.GET)
    
    if form.is_valid():
        query = form.cleaned_data['query']

        print("Search Query:", query)

        # Filter books based on the search query in titles
        results = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
        print("Results:", results)
    else:
        results = Book.objects.all()

    return render(request, 'books.html', {'form': form, 'books': results})

def filtered_books(request, title_query):
    
    if title_query == 'all':
        books = Book.objects.all()
    else:
    # Filtering books based on title containing the query
        category_books = Book.objects.filter(Q(title__icontains=title_query))
        books=category_books
    return render(request, 'filtered_books.html', {'books': books, 'title_query': title_query})

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def save_book(request, book_title):
     
    if request.user.is_authenticated:
        book = get_object_or_404(Book, title=book_title)
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        user_profile.saved_books.add(book)
    return redirect('filtered_books', title_query=book_title)

def remove_book(request, book_title):
    if request.user.is_authenticated:
        try:
            book = Book.objects.get(title=book_title)
            request.user.userprofile.saved_books.remove(book)
            # You might want to redirect to the dashboard or a success page
            return redirect('dashboard')
        except Book.DoesNotExist:
            # Handle the case where the book doesn't exist
            pass
    # Handle authentication or other error cases
    return redirect('dashboard')  # Redirect to the dashboard in case of er



