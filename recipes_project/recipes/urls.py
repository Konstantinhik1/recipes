from django.urls import path
from . import views  # Импортируем модуль views из текущего приложения

from django.urls import path
from . import views  # Импортируем модуль views из текущего приложения

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница
    path('recipes/', views.recipe_catalog, name='recipe_catalog'),  # Каталог рецептов
    path('recipes/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),  # Детали рецепта
    path('ingredients/<int:ingredient_id>/', views.ingredient_detail, name='ingredient_detail'),  # Ингредиенты
]


