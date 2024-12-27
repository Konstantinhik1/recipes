from django.urls import path
from .views import index  # Импортируем представление index из views.py

urlpatterns = [
    path('', index, name='index'),  # Главная страница
]

