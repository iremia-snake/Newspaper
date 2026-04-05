from django.shortcuts import render, HttpResponse
from news.models import Article
# Create your views here.


def index(request):
    news = Article.objects.all()
    data = {
        'title': 'главная',
        'news': news,
    }
    return render(request, 'main/index.html', data)

def about(request):
    return render(request, 'main/about.html')
