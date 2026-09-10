from django.shortcuts import render


def home(request):
    return render(request, 'core/board.html')


def history(request):
    return render(request, 'core/history.html')


def categories(request):
    return render(request, 'core/categories.html')
