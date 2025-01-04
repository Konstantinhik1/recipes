from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, Step
from .forms import RecipeForm


def index(request):
    return render(request, 'recipes/index.html', {'title': 'Главная страница сайта рецептов'})


def recipe_catalog(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/recipe_catalog.html', {'recipes': recipes})


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})


def recipe_add(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.created_by = request.user
            recipe.save()

            steps = recipe.instructions.splitlines()  # Разделяем строки на шаги
            for step_number, description in enumerate(steps, start=1):
                if description.strip():
                    Step.objects.create(recipe=recipe, step_number=step_number, description=description)
            return redirect('recipe_catalog')
    else:
        form = RecipeForm()

    return render(request, 'recipes/recipe_form.html', {'form': form, 'title': 'Добавить рецепт'})


def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()

            recipe.detailed_steps.all().delete()  # Удаляем старые шаги
            steps = recipe.instructions.splitlines()
            for step_number, description in enumerate(steps, start=1):
                if description.strip():
                    Step.objects.create(recipe=recipe, step_number=step_number, description=description)

            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)

    return render(request, 'recipes/recipe_form.html', {'form': form, 'title': 'Редактировать рецепт'})
