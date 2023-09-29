from django import forms
from django_filters import FilterSet, ModelMultipleChoiceFilter
from stores.models import Store, StoreID


class StoreFilter(FilterSet):
    store = ModelMultipleChoiceFilter(
        queryset=StoreID.objects.all(),
        to_field_name='title',
        field_name='store__title',
        widget=forms.CheckboxSelectMultiple,
        label='хэш ID',
    )
    
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

