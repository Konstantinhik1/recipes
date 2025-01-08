from django import forms
from .models import Recipe, Category, Review


class RecipeForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Категории"
    )

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients_text', 'instructions', 'preparation_time', 'image', 'categories']
        widgets = {
            'instructions': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Введите шаги приготовления, разделяя их новой строкой'
            }),
        }


class RecipeFilterForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label="Выберите категорию"
    )


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Напишите ваш отзыв'
            }),
        }
