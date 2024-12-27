from django.shortcuts import render

def index(request):
    return render(request, 'recipes/index.html', {'title': 'Главная страница сайта рецептов'})


