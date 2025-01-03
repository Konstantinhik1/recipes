from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница
    path('recipes/', views.recipe_catalog, name='recipe_catalog'),  # Каталог рецептов
    path('recipes/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),  # Детали рецепта
    path('recipes/add/', views.recipe_add, name='recipe_add'),  # Добавление рецепта
    path('recipes/<int:recipe_id>/edit/', views.recipe_edit, name='recipe_edit'),  # Редактирование рецепта

]


