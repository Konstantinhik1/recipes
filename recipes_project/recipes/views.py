from django.shortcuts import render, get_object_or_404, redirect
from .models import Ingredient, Recipe
from .forms import RecipeForm

def index(request):
    return render(request, 'recipes/index.html', {'title': 'Главная страница сайта рецептов'})


# Отображение каталога рецептов
def recipe_catalog(request):
    recipes = Recipe.objects.all()  # Получаем все рецепты
    return render(request, 'recipes/recipe_catalog.html', {'recipes': recipes})


# Отображение деталей рецепта
def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)  # Получаем рецепт по ID
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})


# Отображение деталей ингредиента
def ingredient_detail(request, ingredient_id):
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)
    return render(request, 'recipes/ingredient_detail.html', {'ingredient': ingredient})


# Добавление рецепта
def recipe_add(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            # Сохранение рецепта
            recipe = form.save(commit=False)
            recipe.created_by = request.user
            recipe.save()
            form.save_m2m()

            # Обработка нового ингредиента и его количества
            new_ingredient = request.POST.get('new_ingredient')
            ingredient_quantity = request.POST.get('ingredient_quantity')

            if new_ingredient and ingredient_quantity:
                try:
                    quantity = float(ingredient_quantity)
                except ValueError:
                    quantity = None

                if quantity is not None:
                    ingredient, created = Ingredient.objects.get_or_create(name=new_ingredient)
                    # Здесь можно обработать граммовку (например, сохранить её в связующей таблице)
                    recipe.ingredients.add(ingredient)

            return redirect('recipe_catalog')
    else:
        form = RecipeForm()

    return render(request, 'recipes/recipe_form.html', {'form': form, 'title': 'Добавить рецепт'})


# Редактирование рецепта
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()

            # Обработка нового ингредиента
            new_ingredient = request.POST.get('new_ingredient')
            ingredient_quantity = request.POST.get('ingredient_quantity')

            if new_ingredient and ingredient_quantity:
                try:
                    quantity = float(ingredient_quantity)
                except ValueError:
                    quantity = None

                if quantity is not None:
                    ingredient, created = Ingredient.objects.get_or_create(name=new_ingredient)
                    recipe.ingredients.add(ingredient)

            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)

    return render(request, 'recipes/recipe_form.html', {'form': form, 'title': 'Редактировать рецепт'})
