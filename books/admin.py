from django.contrib import admin


# Register your models here
from .models import Book,KannadaBook,SELFHELP_BOOK,CHILDREN

admin.site.register(Book)
admin.site.register(KannadaBook)
admin.site.register(SELFHELP_BOOK)
admin.site.register(CHILDREN)