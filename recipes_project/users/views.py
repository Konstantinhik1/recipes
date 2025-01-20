from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from .models import UserSession

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Вы успешно зарегистрировались!")
            return redirect('login')
        else:
            messages.error(request, "Ошибка регистрации. Проверьте введенные данные.")
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:  # Проверяем, если пользователь уже авторизован
        # Если пользователь авторизован, выводим сообщение с предложением выйти
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
                # Проверка сессии
                user_session, created = UserSession.objects.get_or_create(user=user)
                if user_session.is_logged_in:
                    messages.error(request, "Этот пользователь уже авторизован в системе.")
                    return redirect('login')
                else:
                    # Завершаем все активные сессии
                    UserSession.objects.filter(is_logged_in=True).update(is_logged_in=False)

                    # Устанавливаем текущую сессию как активную
                    user_session.is_logged_in = True
                    user_session.save()

                    login(request, user)
                    messages.success(request, "Вы успешно вошли!")
                    return redirect('index')  # Перенаправление на главную
            else:
                messages.error(request, "Неверное имя пользователя или пароль.")
        else:
            messages.error(request, "Ошибка в форме. Проверьте данные.")
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    if request.user.is_authenticated:
        user_session = UserSession.objects.filter(user=request.user).first()
        if user_session:
            user_session.is_logged_in = False
            user_session.save()

    logout(request)
    messages.success(request, "Вы успешно вышли из системы.")
    return redirect('login')
