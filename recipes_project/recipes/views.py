from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from .models import Recipe, Step, Category, Review
from .forms import RecipeForm, RecipeFilterForm, ReviewForm
from django.contrib.auth.decorators import login_required


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
    reviews = Review.objects.filter(recipe=recipe)
    review_form = ReviewForm()

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.recipe = recipe
            review.author = request.user
            review.save()
            return redirect('recipe_detail', recipe_id=recipe.id)

    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'reviews': reviews,
        'review_form': review_form,
        'user': request.user,  # Передаем текущего пользователя
    })


@login_required
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


@login_required
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if recipe.created_by != request.user:
        return HttpResponseForbidden("Вы не можете редактировать этот рецепт.")

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


@login_required
def review_edit(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.author != request.user:
        return HttpResponseForbidden("Вы не можете редактировать этот отзыв.")

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('recipe_detail', recipe_id=review.recipe.id)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'recipes/review_form.html', {'form': form, 'title': 'Редактировать отзыв'})


@login_required
def review_delete(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.author != request.user:
        return HttpResponseForbidden("Вы не можете удалить этот отзыв.")

    recipe_id = review.recipe.id
    review.delete()
    return redirect('recipe_detail', recipe_id=recipe_id)
