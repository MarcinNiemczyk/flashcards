from django.contrib import admin
from .models import Collection, Flashcard, Log, Setting


class FlashcardInline(admin.StackedInline):
    model = Flashcard
    fields = ('task', 'solution')


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    filter_horizontal = ('followers',)
    list_display = ('title', 'author', 'public')
    list_filter = ('public',)
    save_on_top = True
    search_fields = ('title',)
    inlines = [
        FlashcardInline,
    ]


@admin.register(Log)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('id', 'visitor', 'collection', 'timestamp')


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('collection', 'user')
