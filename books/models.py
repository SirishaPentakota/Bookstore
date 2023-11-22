from django.db import models

from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    
    pdf = models.FileField(blank=True, upload_to='book/pdfs', max_length=100)
    cover = models.ImageField(upload_to='book/covers', height_field=None, width_field=None, max_length=None)
    flipkart_url = models.URLField(blank=True)
    
    # Add the price field
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.pdf.delete()
        self.cover.delete()
        super().delete(*args, **kwargs)


   
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    saved_books = models.ManyToManyField(Book)
    # Assuming you have a Book model

class KannadaBook(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.IntegerField(max_length=10)
    pdf = models.FileField(blank=True,upload_to='book/pdfs', max_length=100)
    cover = models.ImageField(upload_to='book/covers', height_field=None, width_field=None, max_length=None)
    flipkart_url = models.URLField(blank=True)
    language = models.CharField(max_length=50, default='Kannada')

    # Add other fields specific to Kannada books as needed

    def __str__(self):
        return self.title
    
class SELFHELP_BOOK(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.IntegerField(max_length=10)
    pdf = models.FileField(blank=True,upload_to='book/pdfs', max_length=100)
    cover = models.ImageField(upload_to='book/covers', height_field=None, width_field=None, max_length=None)
    flipkart_url = models.URLField(blank=True)
    language = models.CharField(max_length=50, default='selfhelp')

    def __str__(self):
        return self.title
    
class CHILDREN(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.IntegerField(max_length=10)
    pdf = models.FileField(blank=True,upload_to='book/pdfs', max_length=100)
    cover = models.ImageField(upload_to='book/covers', height_field=None, width_field=None, max_length=None)
    flipkart_url = models.URLField(blank=True)
    language = models.CharField(max_length=50, default='children')

    def __str__(self):
        return self.title
    
class TodoItem(models.Model):
    book_title = models.CharField(max_length=255)
    concept = models.CharField(max_length=255)
    page_number = models.PositiveIntegerField()