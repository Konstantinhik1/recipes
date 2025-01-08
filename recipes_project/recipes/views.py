from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, Step, Category, Review
from .forms import RecipeForm, RecipeFilterForm, ReviewForm


def index(request):
    return render(request, 'recipes/index.html', {'title': 'Главная страница сайта рецептов'})


def recipe_catalog(request):
    recipes = Recipe.objects.all()
    filter_form = RecipeFilterForm(request.GET)
    if filter_form.is_valid() and filter_form.cleaned_data['category']:
        category = filter_form.cleaned_data['category']
        recipes = recipes.filter(categories=category)

    return render(request, 'recipes/recipe_catalog.html', {
        'recipes': recipes,
        'filter_form': filter_form,
    })


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    reviews = recipe.reviews.all()

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.recipe = recipe
            review.save()
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        review_form = ReviewForm()

    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'reviews': reviews,
        'review_form': review_form
    })


def recipe_add(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.created_by = request.user
            recipe.save()
            form.save_m2m()

            steps = recipe.instructions.splitlines()
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
            recipe = form.save(commit=False)
            recipe.save()
            form.save_m2m()

            recipe.detailed_steps.all().delete()
            steps = recipe.instructions.splitlines()
            for step_number, description in enumerate(steps, start=1):
                if description.strip():
                    Step.objects.create(recipe=recipe, step_number=step_number, description=description)
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)

    return render(request, 'recipes/recipe_form.html', {'form': form, 'title': 'Редактировать рецепт'})
