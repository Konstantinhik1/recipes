from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Email",
        error_messages={
            'required': 'Это поле обязательно.',
            'invalid': 'Введите правильный адрес электронной почты.',
        }
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        error_messages = {
            'username': {
                'required': 'Введите имя пользователя.',
                'unique': 'Пользователь с таким именем уже существует.',
            },
            'password1': {
                'required': 'Введите пароль.',
            },
            'password2': {
                'required': 'Подтвердите пароль.',
                'password_mismatch': 'Пароли не совпадают.',
            },
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Имя пользователя",
        error_messages={
            'required': 'Введите имя пользователя.',
        }
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        error_messages={
            'required': 'Введите пароль.',
        }
    )