from django.urls import path
from . import views

# app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/',  views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.user_view, name='profile'),
    path('profile/edit/', views.user_edit_view, name='profile_edit'),
    path('users/<slug:username>/', views.profile_view, name='show_user'),
]
