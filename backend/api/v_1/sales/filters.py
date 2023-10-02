from django_filters import rest_framework as filters
from sales.models import Sales


class SalesFilter(filters.FilterSet):
    store = filters.CharFilter(field_name="store__store")
    sku = filters.CharFilter(field_name="sku__sku")
    date = filters.DateFilter(field_name="fact__date")
    sales_type = filters.NumberFilter(field_name="fact__sales_type")
    sales_units = filters.NumberFilter(field_name="fact__sales_units")
    sales_units_promo = filters.NumberFilter(field_name="fact__sales_units_promo")
    sales_rub = filters.NumberFilter(field_name="fact__sales_rub")
    sales_run_promo = filters.NumberFilter(field_name="fact__sales_run_promo")

    class Meta:
        model = Sales
        fields = [
            'store', 
            'sku', 
            'date', 
            'sales_type', 
            'sales_units', 
            'sales_units_promo', 
            'sales_rub', 
            'sales_run_promo'
            ]