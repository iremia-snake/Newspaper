from django.urls import path
from . import views

urlpatterns = [
    path('new_article', views.new_article, name='add_article'),
    path('edit/<int:pk>', views.edit_article, name='edit_article'),
    path('<int:pk>', views.show_article, name='show_article'),
    path('newspaper', views.newspaper, name='newspaper'),
    path('', views.news_home, name='news'),
]