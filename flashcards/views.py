import json
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Collection, Flashcard


def explore(request):
    return render(request, 'flashcards/explore.html')


@login_required
def library(request):
    return render(request, 'flashcards/library.html')


@login_required
def add_collection(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'Invalid request'
            }, status=400)

        title = data['title']
        if title.rstrip() == '' or len(title) > 150:
            return JsonResponse({
                'error': 'Invalid title'
            }, status=400)

        visibility = data['visibility']
        if visibility != 'Public' and visibility != 'Private':
            return JsonResponse({
                'error': 'Invalid visibility'
            }, status=400)
        public = True if visibility == 'Public' else False

        collection = Collection(
            author=request.user,
            title=title,
            public=public
        )
        collection.save()

        flashcards = data['flashcards']
        if len(flashcards) < 2:
            return JsonResponse({
                'error': 'At least 2 flashcards required'
            })
        for flashcard in flashcards:
            f = Flashcard(
                task=flashcard['task'],
                solution=flashcard['solution'],
                collection=collection
            )
            f.save()
        return JsonResponse({
            'success': 'Collection added successfully.'
        }, status=201)

    return render(request, 'flashcards/add_collection.html')
