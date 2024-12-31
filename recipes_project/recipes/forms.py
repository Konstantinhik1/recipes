from django import forms
from .models import Recipe, Ingredient

class RecipeForm(forms.ModelForm):
    new_ingredient = forms.CharField(
        max_length=200,
        required=False,
        help_text="Введите новый ингредиент, если его нет в списке.",
        widget=forms.TextInput(attrs={'id': 'id_new_ingredient'})  # Добавляем id атрибут
    )

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'preparation_time', 'image']
        widgets = {
            'ingredients': forms.CheckboxSelectMultiple(),  # Множественный выбор ингредиентов
        }
