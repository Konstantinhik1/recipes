from django.db import models
from django.contrib.auth.models import User


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    ingredients_text = models.TextField(default="")
    preparation_time = models.PositiveIntegerField(help_text="Время на приготовление (в минутах)")
    instructions = models.TextField(default="", help_text="Опишите шаги приготовления, разделенные новой строкой.")
    image = models.ImageField(upload_to='recipes_images/', blank=True, null=True)

    def __str__(self):
        return self.title


class Step(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='detailed_steps',
        on_delete=models.CASCADE
    )
    step_number = models.PositiveIntegerField()
    description = models.TextField()

    class Meta:
        ordering = ['step_number']

    def __str__(self):
        return f"Шаг {self.step_number} для {self.recipe.title}"
