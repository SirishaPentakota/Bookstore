from django.db import models

from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    pdf = models.FileField(blank=True,upload_to='book/pdfs', max_length=100)
    cover = models.ImageField(upload_to='book/covers', height_field=None, width_field=None, max_length=None)
    flipkart_url = models.URLField(blank=True)

    def __str__(self):
        return self.title
    
    def delete(self,*args,**kwargs):
        self.pdf.delete()
        self.cover.delete()
        super().delete(*args,**kwargs)

   
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    saved_books = models.ManyToManyField(Book)  # Assuming you have a Book model

