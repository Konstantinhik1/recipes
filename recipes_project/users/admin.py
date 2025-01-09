from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Удаляем стандартную регистрацию
admin.site.unregister(User)

# Создаем свой кастомный класс
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Добавьте свои изменения, если нужно
    pass
