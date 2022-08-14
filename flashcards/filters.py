import django_filters
from .models import Collection


class CollectionFilter(django_filters.FilterSet):

    SORTING_CHOICES = (
        ('newest', 'Newest'),
        ('oldest', 'Oldest'),
    )

    sorting = django_filters.ChoiceFilter(
        label='Sort by',
        choices=SORTING_CHOICES,
        method='sort_collections')

    class Meta:
        model = Collection
        fields = {
            'title': ['icontains'],
        }

    def sort_collections(self, queryset, name, value):
        expression = 'id' if value == 'oldest' else '-id'
        return queryset.order_by(expression)
