from django.contrib import admin
from .models import Flashcard, Collection


class FlashcardInline(admin.StackedInline):
    model = Flashcard
    fields = ('task', 'solution')


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    filter_horizontal = ('followers',)
    list_display = ('title', 'author', 'public')
    inlines = [
        FlashcardInline,
    ]
    search_fields = ('title',)
    list_filter = ('public',)
