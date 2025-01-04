from django.contrib import admin
from .models import Recipe, Step, Category


class StepInline(admin.TabularInline):
    model = Step
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'preparation_time')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'created_by', 'categories')
    inlines = [StepInline]
