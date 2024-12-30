from django.shortcuts import render

def index(request):
    return render(request, 'recipes/index.html', {'title': 'Главная страница сайта рецептов'})


from django.shortcuts import render, get_object_or_404
from .models import Recipe


# Отображение каталога рецептов
def recipe_catalog(request):
    recipes = Recipe.objects.all()  # Получаем все рецепты
    return render(request, 'recipes/recipe_catalog.html', {'recipes': recipes})


# Отображение деталей рецепта
def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)  # Получаем рецепт по ID
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})

from django.shortcuts import render, get_object_or_404
from .models import Ingredient, Recipe

def ingredient_detail(request, ingredient_id):
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)
    return render(request, 'recipes/ingredient_detail.html', {'ingredient': ingredient})
