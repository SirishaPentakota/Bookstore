from django.urls import path
from . import views
from .views import  home,register,login_user,logout_user

urlpatterns = [
    path('',home,name='home'),
    path('register/',register,name='register'),
    path('login/', login_user,name='login'),
    path('logout/',logout_user,name='logout'),
    path('add_book/', views.add_book, name='add_book'),
    path('books/', views.book_list, name='book_list'),
    path('/', views.book_search_view, name='book_search'),
    path('filtered_books/<str:title_query>/', views.filtered_books, name='filtered_books'),
    path('Cart/', views.dashboard, name='dashboard'),
    path('save_book/<str:book_title>/', views.save_book, name='save_book'),
    path('remove_book/<str:book_title>/', views.remove_book, name='remove_book'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
]


