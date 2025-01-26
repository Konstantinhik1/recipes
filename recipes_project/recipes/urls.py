from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница
    path('catalog/', views.recipe_catalog, name='recipe_catalog'),  # Каталог рецептов
    path('recipe/add/', views.recipe_add, name='recipe_add'),  # Добавление рецепта
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),  # Детали рецепта
    path('recipe/<int:recipe_id>/edit/', views.recipe_edit, name='recipe_edit'),  # Редактирование рецепта
    path('reviews/<int:review_id>/update/', views.update_review, name='review_update'),  # Редактирование отзыва
    path('review/<int:review_id>/delete/', views.review_delete, name='review_delete'),  # Удаление отзыва
]
