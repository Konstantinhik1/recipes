from django.db import models
from django.contrib.auth.models import User


# Модель ингредиента
class Ingredient(models.Model):
    name = models.CharField(max_length=200)  # Название ингредиента
    description = models.TextField(blank=True)  # Описание (например, если ингредиент требует подготовки)

    def __str__(self):
        return self.name


# Модель рецепта
class Recipe(models.Model):
    title = models.CharField(max_length=200)  # Название рецепта
    description = models.TextField()  # Описание рецепта
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Пользователь, который создал рецепт
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания рецепта
    ingredients = models.ManyToManyField(Ingredient)  # Связь многие ко многим с ингредиентами
    preparation_time = models.PositiveIntegerField(help_text="Время на приготовление (в минутах)")  # Время приготовления
    image = models.ImageField(upload_to='recipes_images/', blank=True, null=True)  # Изображение

    def __str__(self):
        return self.title


# Модель шагов рецепта
class Step(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='steps', on_delete=models.CASCADE)  # Рецепт, к которому относится шаг
    step_number = models.PositiveIntegerField()  # Номер шага
    description = models.TextField()  # Описание шага

    class Meta:
        ordering = ['step_number']  # Сортировать по порядку шагов

    def __str__(self):
        return f"Шаг {self.step_number} для {self.recipe.title}"
