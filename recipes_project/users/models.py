from django.contrib.auth.models import User
from django.db import models

class UserSession(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='session',
        unique=True  # Уникальная связь между пользователем и сессией
    )
    is_logged_in = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {'Logged In' if self.is_logged_in else 'Logged Out'}"
