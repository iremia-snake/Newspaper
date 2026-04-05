from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Article
from .forms import ArticleForm, SearchForm
import markdown
import datetime


def search(queryset, search_query):
    if not search_query:
        return queryset

    matching_ids = []
    # Оптимизация: берем только нужные поля
    for obj in queryset.only('id', 'title').iterator():
        if search_query.lower() in obj.title.lower():
            matching_ids.append(obj.id)

    return queryset.filter(id__in=matching_ids)


def news_home(request):
    article_list = Article.objects.all()

    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        search_query = search_form.cleaned_data['search_query']
        article_list = search(article_list, search_query)

    # filter_form = CombinedFilterForm(request.GET)
    # if filter_form.is_valid():
    #     date_range = filter_form.cleaned_data['date_range']
    #     if date_range:
    #         date_start, date_end = date_range.split(' - ')
            # article_list = article_list.filter()

    data = {
        'news_list': article_list,
        'search_form': search_form,
        'filter_form': '',
    }
    return render(request, 'news/news.html', data)


def md_to_html(md_text):
    """Конвертирует Markdown в чистый HTML """
    extensions = [
        'tables',
        'mdx_truly_sane_lists',
        'fenced_code',
        'footnotes',
        # 'attr_list',
    ]
    extension_configs = {
        'mdx_truly_sane_lists': {
            'nested_indent': 2,
            'truly_sane': True,
        }
    },

    html = markdown.markdown(
        md_text,
        extensions=extensions
    )
    return html


def show_article(request, pk):
    article = Article.objects.get(pk=pk)
    html = md_to_html(article.content)
    article.content = html
    data = {
        'article': article
    }
    return render(request, 'news/show_article.html', data)


@login_required
def new_article(request):
    error = ''
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.date = datetime.datetime.now()
            article.author = request.user
            form.save()
            return redirect('news')
        else:
            error = 'Форма заполнена неверно'
            error += form.errors.as_text()
    form = ArticleForm()
    data = {'form': form, 'error': error}
    return render(request, 'news/create.html', data)


# @login_required
def edit_article(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, 'Вы не вошли в систему')
        return redirect('news')
    error = ''
    article_object = Article.objects.get(pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article_object)
        if form.is_valid():
            article = form.save(commit=False)
            article.date = datetime.datetime.now()
            form.save()
            return redirect('news')
        else:
            error = 'Форма заполнена неверно'
            error += form.errors.as_text()
    form = ArticleForm(instance=article_object)
    data = {'form': form, 'error': error}
    return render(request, 'news/create.html', data)
    # return HttpResponse("<p>test</p>")

def newspaper(request):
    return render(request, 'news/newspaper.html')