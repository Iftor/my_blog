from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from . import models


User = get_user_model()


class RegisterForm(UserCreationForm):
    """Форма регистрации"""
    firstname = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'registration-form__input',
            'placeholder': 'Имя',
        }),
    )
    lastname = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'registration-form__input',
            'placeholder': 'Фамилия',
        }),
    )
    password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'registration-form__input',
            'placeholder': 'Пароль',
        }),
    )
    password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'registration-form__input',
            'placeholder': 'Подтверждение пароля',
        }),
    )

    class Meta:
        model = User
        fields = ('username', 'firstname', 'lastname', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'registration-form__input',
                'placeholder': 'Имя пользователя',
            }),
        }


class AddPostForm(forms.ModelForm):
    """Форма добавления новой публикации"""

    class Meta:
        model = models.BlogPost
        fields = ('text', )
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'add-pub-form__input',
                'placeholder': 'Текст публикации',
            }),
        }


class UserLoginForm(AuthenticationForm):
    """Форма авторизации"""
    username = UsernameField(
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'class': 'login-form__input',
            'placeholder': 'Имя пользователя',
        }),
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'class': 'login-form__input',
            'placeholder': 'Пароль',
        }),
    )
