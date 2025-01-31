from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=18)
    description = models.TextField(blank=True, null=True)
    ingredients_text = models.TextField(help_text="Список ингредиентов, каждый ингредиент на новой строке")
    instructions = models.TextField()  # Поле для инструкций
    preparation_time = models.IntegerField()
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    categories = models.ManyToManyField('Category', related_name='recipes')
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Step(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='detailed_steps')
    step_number = models.PositiveIntegerField()
    description = models.TextField()

    class Meta:
        ordering = ['step_number']

    def __str__(self):
        return f"Step {self.step_number} for {self.recipe.title}"


class Review(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.author.username} on {self.recipe.title}"
