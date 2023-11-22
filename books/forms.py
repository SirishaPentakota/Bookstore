from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author','price','pdf', 'cover','flipkart_url']
        

class BookSearchForm(forms.Form):
    query = forms.CharField(max_length=100, label='Search')
    subjects = forms.MultipleChoiceField(choices=[], widget=forms.CheckboxSelectMultiple(), required=False)

    def __init__(self, *args, **kwargs):
        categories = kwargs.pop('categories', [])
        super(BookSearchForm, self).__init__(*args, **kwargs)
        self.fields['subjects'].choices = [(category, category) for category in categories]
