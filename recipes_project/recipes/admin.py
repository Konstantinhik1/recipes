from django.contrib import admin

from django.contrib import admin
from .models import Ingredient, Recipe, Step


# Настройка админки для модели Ingredient
@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Отображать только название
    search_fields = ('name',)  # Поиск по названию


# Настройка админки для модели Step
class StepInline(admin.TabularInline):
    model = Step
    extra = 1  # Количество дополнительных пустых строк для добавления шагов


# Настройка админки для модели Recipe
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'preparation_time')  # Поля для отображения
    search_fields = ('title', 'description')  # Поля для поиска
    list_filter = ('created_at', 'created_by')  # Фильтры
    inlines = [StepInline]  # Добавление шагов в админку рецепта

