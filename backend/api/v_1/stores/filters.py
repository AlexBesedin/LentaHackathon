import django_filters
from stores.models import Store


class StoreFilter(django_filters.FilterSet):
    store = django_filters.CharFilter(field_name="store")
    city = django_filters.CharFilter(field_name="city")
    division = django_filters.CharFilter(field_name="division")
    type_format = django_filters.NumberFilter(field_name="type_format__id")
    loc = django_filters.NumberFilter(field_name="loc__loc")
    size = django_filters.NumberFilter(field_name="size__size")
    is_active = django_filters.BooleanFilter(field_name="is_active__is_active")

    class Meta:
        model = Store
        fields = ['store', 'city', 'division', 'type_format',
                  'loc', 'size', 'is_active', ]
