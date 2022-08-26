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

    paginator = Paginator(collections_filter.qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Remove page from query to apply current filter while switching pages
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

    # Assign sorted collections
    collections = [item.collection for item in items]

    paginator = Paginator(collections, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'flashcards/library.html', {
        'collections': page_obj
    })


@login_required
def add_collection(request):
    if request.method == 'POST':
        data = load_collection_form(request)
        if 'error' in data:
            return JsonResponse({
                'error': data['error']
            }, status=data['status'])

        # Create new collection
        collection = Collection(
            author=request.user,
            title=data['title'],
            public=data['visibility'],
            language1=data['language1'],
            language2=data['language2']
        )
        collection.save()

        # Add flashcards
        for flashcard in data['flashcards']:
            task = flashcard['task']
            solution = flashcard['solution']
            f = Flashcard(
                task=task,
                solution=solution,
                collection=collection
            )
            f.save()

        # Create new visit log as creation time
        visit = Log(visitor=request.user, collection=collection)
        visit.save()

        return JsonResponse({
            'success': 'Collection added successfully.'
        }, status=201)

    return render(request, 'flashcards/add.html', {
        'languages': LANGUAGES
    })


@login_required
def edit_collection(request, collection_id):
    try:
        collection = Collection.objects.get(id=collection_id)
    except Collection.DoesNotExist:
        raise Http404('Collection not found')

    # Ensure user is an author
    if not request.user.is_authenticated or request.user != collection.author:
        return HttpResponseForbidden()

    if request.method == 'PUT':
        # Load data
        data = load_collection_form(request)
        if 'error' in data:
            return JsonResponse({
                'error': data['error']
            }, status=data['status'])

        # Load collection
        collection = Collection.objects.get(id=collection_id)

        # Update collection
        collection.title = data['title']
        collection.public = data['visibility']
        collection.language1 = data['language1']
        collection.language2 = data['language2']
        collection.save()

        # Replace flashcards
        collection.flashcards.all().delete()
        for flashcard in data['flashcards']:
            task = flashcard['task']
            solution = flashcard['solution']
            f = Flashcard(
                task=task,
                solution=solution,
                collection=collection
            )
            f.save()

        # Update logs
        log = Log.objects.get(visitor=request.user, collection=collection)
        log.timestamp = datetime.now()
        log.save()

        return JsonResponse({
            'success': 'Collection updated successfully'
        }, status=201)

    return render(request, 'flashcards/edit.html', {
        'collection': collection,
        'languages': LANGUAGES
    })


def load_collection_form(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return {'error': 'Invalid request', 'status': 400}

    # Prevent client from sending wrong request data
    try:
        title = data['title'].rstrip()
        visibility = data['visibility']
        language1 = data['language1']
        language2 = data['language2']
        flashcards = data['flashcards']
    except KeyError:
        return {'error': 'Invalid data request', 'status': 400}

    # Ensure title length is correct
    if not title:
        return {'error': 'Title cannot be empty', 'status': 400}
    elif len(title) > 100:
        return {'error': 'Title too long', 'status': 400}

    # Validate visibility
    if visibility != 'Public' and visibility != 'Private':
        return {'error': 'Invalid visibility', 'status': 400}
    public = True if visibility == 'Public' else False

    # Ensure languages are listed
    if language1 not in LANGUAGES or language2 not in LANGUAGES:
        return {'error': 'Invalid language', 'status': 400}

    # Check minimum flashcards per collection
    if len(flashcards) < MIN_FLASHCARDS:
        return {
            'error': f'At least {MIN_FLASHCARDS} flashcards required',
            'status': 400
        }

    collection_data = {
        'title': title,
        'visibility': public,
        'language1': language1.lower(),
        'language2': language2.lower(),
        'flashcards': flashcards
    }
    return collection_data


def collection_details(request, collection_id):
    try:
        collection = Collection.objects.get(id=collection_id)
    except Collection.DoesNotExist:
        raise Http404('Collection not found')

    # Ensure user cannot access other private collections
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
