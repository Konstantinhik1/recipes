from django import forms
from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients_text', 'instructions', 'preparation_time', 'image']
        widgets = {
            'instructions': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Введите шаги приготовления, разделяя их новой строкой'
            }),
        }
