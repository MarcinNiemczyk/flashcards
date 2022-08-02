from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from .models import Collection, Flashcard


def explore(request):
    return render(request, 'flashcards/explore.html')


@login_required
def library(request):
    return render(request, 'flashcards/library.html')


@login_required
def add_collection(request):
    if request.method == 'POST':
        data = request.POST
        # TODO: Data validation
        # collection = Collection(author=request.user)
        # for item in data:
        #     if item != 'csrfmiddlewaretoken':
        #         if item == 'title':
        #             collection.title = request.POST[item]
        #         elif item == 'visibility':
        #             visibility = request.POST[item]
        #             if visibility == 'public':
        #                 public = True
        #             else:
        #                 public = False
        #             collection.public = public
        #             collection.save()
        #         else:
        #             task, solution = request.POST.getlist(item)
        #             flashcard = Flashcard(
        #                 collection=collection,
        #                 task=task,
        #                 solution=solution
        #             )
        #             flashcard.save()

    return render(request, 'flashcards/add_collection.html')
