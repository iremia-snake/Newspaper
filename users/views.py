from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PersonCreationForm, PersonEditForm, LoginForm
from .models import Person
from django.template.loader import get_template


def register_view(request):
    if request.method == 'POST':
        form = PersonCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('home')
    else:
        form = PersonCreationForm()

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                # messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    # print("Да почему я 4 года учился на программиста, мне это нравится, а по итогу я - хуй без палочки, не могу оди ебаный сайтик уровня восьмилетки написать???????")
    if request.user.is_authenticated:
        logout(request)
    # messages.info(request, 'Вы вышли из системы')
    return redirect('login')


# @login_required
def user_view(request):
    if request.user.is_authenticated:
        return render(request, 'users/profile.html', {'profile': request.user})
    return redirect('login')


@login_required
def user_edit_view(request):
    user = request.user

    if request.method == 'POST':
        form = PersonEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные обновлены!')
            return redirect('profile')
    else:
        form = PersonEditForm(instance=user)

    data = {
        'form': form,
        'profile': user,
    }
    return render(request, 'users/profile_edit.html', data)


def profile_view(request, username):
    return render(request, 'users/profile.html', {'profile': Person.objects.get(username=username)})
