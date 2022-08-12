import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from .models import Collection, Flashcard, Log


def explore(request):
    collections = Collection.objects.filter(public=True).order_by('-id').all()

    paginator = Paginator(collections, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'flashcards/explore.html', {
        'collections': page_obj
    })


@login_required
def library(request):
    # Sort collections by latest visit
    items = Log.objects.filter(
        visitor=request.user).select_related('visitor').filter(
        Q(collection__author=request.user)
        | Q(collection__followers=request.user)
    ).order_by('-timestamp')

    collections = [item.collection for item in items]
    paginator = Paginator(collections, 10)
    page_number = request.GET.get('page')
    page_library = paginator.get_page(page_number)

    return render(request, 'flashcards/library.html', {
        'collections': page_library
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

        # Update latest visit as creation time
        visit = Log(visitor=request.user, collection=collection)
        visit.save()

        return JsonResponse({
            'success': 'Collection added successfully.'
        }, status=201)

    return render(request, 'flashcards/add.html')
