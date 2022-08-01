from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def explore(request):
    return render(request, 'flashcards/explore.html')


@login_required
def library(request):
    return render(request, 'flashcards/library.html')


@login_required
def add_collection(request):
    return render(request, 'flashcards/add_collection.html')
