from django_filters import FilterSet, AllValuesMultipleFilter, ChoiceFilter, NumberFilter

from stores.models import Store


class StoreFilter(FilterSet):
    store = AllValuesMultipleFilter(field_name='store__title', label='хэш ID')
    city = AllValuesMultipleFilter(field_name="city")
    division = AllValuesMultipleFilter(field_name="division")
    type_format = AllValuesMultipleFilter(field_name="type_format")
    loc = AllValuesMultipleFilter(field_name="loc")
    size = NumberFilter(field_name="size")
    is_active = ChoiceFilter(choices=[(0, 'Неактивный'), (1, 'Активный')])

    
    class Meta:
        model = Store
        fields = [
            'store', 
            'city', 
            'division', 
            'type_format', 
            'loc', 
            'size', 
            'is_active'
        ]

