import django_filters
from django.db.models import Q
from .models import Collection
from flashcards import LANG_CHOICES


class CollectionFilter(django_filters.FilterSet):

    SORTING_CHOICES = (
        ('newest', 'Newest'),
        ('oldest', 'Oldest'),
    )

    sort = django_filters.ChoiceFilter(
        label='Sort by',
        choices=SORTING_CHOICES,
        method='sort_collections')

    language1 = django_filters.ChoiceFilter(
        label='First Language',
        choices=LANG_CHOICES,
        method='filter_language'
    )

    language2 = django_filters.ChoiceFilter(
        label='Second Language',
        choices=LANG_CHOICES,
        method='filter_language'
    )

    class Meta:
        model = Collection
        fields = {
            'title': ['icontains'],
        }

    def sort_collections(self, queryset, name, value):
        expression = 'id' if value == 'oldest' else '-id'
        return queryset.order_by(expression)

    def filter_language(self, queryset, name, value):
        return queryset.filter(
            Q(language1=value)
            | Q(language2=value)
        )
