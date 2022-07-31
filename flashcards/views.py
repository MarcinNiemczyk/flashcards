from django.http import HttpResponse
from django.shortcuts import render


def collections(request):
    return render(request, 'flashcards/collections.html')
