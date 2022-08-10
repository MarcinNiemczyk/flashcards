import json
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Q
from .models import Collection, Flashcard


def explore(request):
    return render(request, 'flashcards/explore.html')


@login_required
def library(request):
    collections = Collection.objects.filter(
        Q(author=request.user)
        | Q(followers=request.user)
    ).order_by('-id')
    return render(request, 'flashcards/library.html', {
        'collections': collections
    })


@login_required
def add_collection(request):
    if request.method == 'POST':
        # Validate input
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'Invalid request'
            }, status=400)

        title = data['title']
        if not title.rstrip():
            return JsonResponse({
                'error': 'Title cannot be empty'
            }, status=400)
        elif len(title) > 100:
            return JsonResponse({
                'error': 'Title too long'
            }, status=400)

        visibility = data['visibility']
        if visibility != 'Public' and visibility != 'Private':
            return JsonResponse({
                'error': 'Invalid visibility'
            }, status=400)
        public = True if visibility == 'Public' else False

        flashcards = data['flashcards']
        if len(flashcards) < 2:
            return JsonResponse({
                'error': 'At least 2 flashcards required'
            }, status=400)

        # Create new collection
        collection = Collection(
            author=request.user,
            title=title,
            public=public
        )
        collection.save()

        # Add flashcards
        for flashcard in flashcards:
            task = flashcard['task']
            solution = flashcard['solution']
            f = Flashcard(
                task=task,
                solution=solution,
                collection=collection
            )
            f.save()
        return JsonResponse({
            'success': 'Collection added successfully.'
        }, status=201)

    return render(request, 'flashcards/add.html')
