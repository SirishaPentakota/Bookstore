from django.urls import path
from . import views
from .views import  home,register,login_user,logout_user,save_book

urlpatterns = [
    path('',home,name='home'),
    path('register/',register,name='register'),
    path('login/', login_user,name='login'),
    path('logout/',logout_user,name='logout'),
    path('add_book/', views.add_book, name='add_book'),
    path('kannada_books/', views.kannada_books, name='kannada_books'),
    path('self_help/', views.selfhelp_books, name='selfhelp_books'),
    path('children/', views.children, name='children'),
    path('save_children_book/<str:book_title>/', views.save_children_book, name='save_children_book'),
    path('save_kannada_book/<str:book_title>/', views.save_kannada_book, name='save_kannada_book'),
    path('save_selfhelp_book/<str:book_title>/', views.save_selfhelp_book, name='save_selfhelp_book'),
    path('all_books/<str:title>/', views.all_books, name='all_books'),
    path('books/', views.book_list, name='book_list'),
    path('/', views.book_search_view, name='book_search'),
    path('Cart/', views.dashboard, name='dashboard'),
    path('save_book/<str:book_title>/', save_book, name='save_book'),
    path('remove_book/<str:book_title>/', views.remove_book, name='remove_book'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
]


