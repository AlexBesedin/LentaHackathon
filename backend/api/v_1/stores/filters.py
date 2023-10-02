from django import forms
from django_filters import FilterSet, ModelMultipleChoiceFilter, CharFilter, NumberFilter, BooleanFilter
from stores.models import Store, StoreID


class StoreFilter(FilterSet):
    store = ModelMultipleChoiceFilter(
        queryset=StoreID.objects.all(),
        to_field_name='title',
        field_name='store__title',
        widget=forms.CheckboxSelectMultiple,
        label='хэш ID',
    )
    city = CharFilter(field_name="city", lookup_expr='exact')
    division = CharFilter(field_name="division", lookup_expr='exact')
    type_format = CharFilter(field_name="type_format", lookup_expr='exact')
    loc = CharFilter(field_name="loc", lookup_expr='exact')
    size = NumberFilter(field_name="size")
    is_active = BooleanFilter(field_name="is_active")
    
    
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

