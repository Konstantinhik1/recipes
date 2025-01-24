from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from .models import UserSession
from django.shortcuts import render

def index(request):
    user_logged_in = request.user.is_authenticated
    username = request.user.username if user_logged_in else None
    return render(request, 'index.html', {'user_logged_in': user_logged_in, 'username': username})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Вы успешно зарегистрировались!")
            return redirect('login')
        else:
            messages.error(request, "Произошла ошибка при регистрации. Проверьте данные.")
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        messages.info(request, "Вы уже вошли в систему.")
        return render(request, 'users/login.html', {'user_logged_in': True})

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                user_session, created = UserSession.objects.get_or_create(user=user)
                if user_session.is_logged_in:
                    messages.error(request, "Этот пользователь уже авторизован в системе.")
                    return redirect('login')
                else:
                    UserSession.objects.filter(user=user, is_logged_in=True).update(is_logged_in=False)
                    user_session.is_logged_in = True
                    user_session.save()
                    login(request, user)
                    return redirect('index')
            else:
                messages.error(request, "Неверное имя пользователя или пароль.")
        else:
            messages.error(request, "Неверное имя пользователя или пароль.")
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    user = request.user
    UserSession.objects.filter(user=user, is_logged_in=True).update(is_logged_in=False)
    logout(request)
    messages.success(request, "Вы успешно покинули систему.")
    return redirect('index')