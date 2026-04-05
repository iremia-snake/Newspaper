from django.urls import path, include
from . import views
import users

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('', include('users.urls'))
]