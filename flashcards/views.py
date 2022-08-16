import json
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import JsonResponse, Http404, HttpResponseForbidden
from django.db.models import Q
from flashcards import LANGUAGES, MIN_FLASHCARDS
from .models import Collection, Flashcard, Log
from .filters import CollectionFilter


def explore(request):

    # Ensure user's own collections are not displayed
    if request.user.is_authenticated:
        collections = Collection.objects.filter(
            public=True).exclude(author=request.user).order_by('-id').all()
    else:
        collections = Collection.objects.filter(
            public=True).order_by('-id').all()

    collections_filter = CollectionFilter(request.GET, queryset=collections)

    # Set pagination
    paginator = Paginator(collections_filter.qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Remove page from query to add filter while switching pages
    request_without_page = request.GET.copy()
    if 'page' in request_without_page:
        del request_without_page['page']
    request.GET = request_without_page

    return render(request, 'flashcards/explore.html', {
        'filter': collections_filter,
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

    # Grab collections from sorted by log date items
    collections = [item.collection for item in items]

    # Set pagination
    paginator = Paginator(collections, 10)
    page_number = request.GET.get('page')
    page_library = paginator.get_page(page_number)

    return render(request, 'flashcards/library.html', {
        'collections': page_library
    })


@login_required
def add_collection(request):
    if request.method == 'POST':
        # Load data
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'Invalid request'
            }, status=400)

        # Prevent client from sending wrong request data
        try:
            title = data['title'].rstrip()
            visibility = data['visibility']
            language1 = data['language1']
            language2 = data['language2']
            flashcards = data['flashcards']
        except KeyError:
            return JsonResponse({
                'error': 'Invalid data request'
            }, status=400)

        # Ensure title length is correct
        if not title:
            return JsonResponse({
                'error': 'Title cannot be empty'
            }, status=400)
        elif len(title) > 100:
            return JsonResponse({
                'error': 'Title too long'
            }, status=400)

        # Validate visibility
        if visibility != 'Public' and visibility != 'Private':
            return JsonResponse({
                'error': 'Invalid visibility'
            }, status=400)
        public = True if visibility == 'Public' else False

        # Ensure languages are listed
        if language1 not in LANGUAGES:
            return JsonResponse({
                'error': 'Invalid question language'
            }, status=400)
        if language2 not in LANGUAGES:
            return JsonResponse({
                'error': 'Invalid answer language'
            }, status=400)

        # Check minimum flashcards per collection
        if len(flashcards) < MIN_FLASHCARDS:
            return JsonResponse({
                'error': f'At least {MIN_FLASHCARDS} flashcards required'
            }, status=400)

        # Create new collection
        collection = Collection(
            author=request.user,
            title=title,
            public=public,
            language1=language1.lower(),
            language2=language2.lower()
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

    return render(request, 'flashcards/add.html', {
        'languages': LANGUAGES
    })


def collection_details(request, collection_id):
    try:
        collection = Collection.objects.get(id=collection_id)
    except Collection.DoesNotExist:
        raise Http404('Collection not found')

    # Ensure user cannot access others private collections
    if request.user != collection.author and not collection.public:
        return HttpResponseForbidden()

    # Update logs for every visit
    if request.user.is_authenticated:
        try:
            log = Log.objects.get(visitor=request.user, collection=collection)
        except Log.DoesNotExist:
            Log.objects.create(
                visitor=request.user,
                collection=collection
            )
        else:
            log.timestamp = datetime.now()
            log.save()

    return render(request, 'flashcards/collection.html', {
        'collection': collection
    })
