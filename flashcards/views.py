from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def library(request):
    return render(request, 'flashcards/library.html')


def explore(request):
    return render(request, 'flashcards/explore.html')
