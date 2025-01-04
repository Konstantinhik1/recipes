from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', views.recipe_catalog, name='recipe_catalog'),  # Каталог рецептов
    path('recipes/', views.recipe_catalog, name='recipe_catalog_redirect'),  # Дублируем маршрут для /recipes/
    path('recipe/add/', views.recipe_add, name='recipe_add'),  # Добавление рецепта
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),  # Детали рецепта
    path('recipe/<int:recipe_id>/edit/', views.recipe_edit, name='recipe_edit'),  # Редактирование рецепта
]


