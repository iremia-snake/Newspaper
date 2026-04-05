from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Person
from os import path
from .widgets import CustomAvatarInput


class PersonCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Person
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'city',
            'password1',
            'password2'
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Person.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует")
        return email


class PersonEditForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'first_name',
            'last_name',
            'email',
            'avatar',
            'bio',
            'city'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
            'avatar': forms.FileInput(),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Проверка, что email не занят другим пользователем
        if Person.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Этот email уже используется другим пользователем")
        return email

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')

        if avatar:
            # Проверка размера файла (макс 2 МБ)
            max_size = 2 * 1024 * 1024  # 2MB
            if avatar.size > max_size:
                raise ValidationError('Размер файла не должен превышать 2 МБ')

            # Проверка расширения файла
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            extension = path.splitext(avatar.name)[1].lower()
            if extension not in valid_extensions:
                raise ValidationError('Поддерживаются только файлы: jpg, jpeg, png, gif')

        return avatar


class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)