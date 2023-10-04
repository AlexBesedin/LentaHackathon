from rest_framework.filters import BaseFilterBackend
from dateutil.parser import parse



class ForecastFilterBackend(BaseFilterBackend):
    """
    Фильтр, который позволяет фильтровать данные прогноза на основе 
    - store (магазин)
    - sku (захэшированное id товара)
    - forecast_date (Дата прогноза)
    - date (Дата(день))
    - target (спрос в ШТ.)
    """

    def filter_queryset(self, request, queryset, view):
        
        store_param = request.query_params.get('store')
        sku_param = request.query_params.get('sku')
        forecast_date_param = request.query_params.get('forecast_date')
        date_param = request.query_params.get('date')
        target_param = request.query_params.get('target')

        
        if store_param is not None:
            store_list = store_param.split(",")
            queryset = queryset.filter(store__store__title__in=store_list)

        #Фильтр хэша товара предсказания
        if sku_param is not None:
            sku_list = sku_param.split(",")
            queryset = queryset.filter(sku__sku__in=sku_list)

        #Фильт даты сформирования предсказания
        if forecast_date_param is not None:
            forecast_date_list = [parse(date_str) for date_str in forecast_date_param.split(",")]
            queryset = queryset.filter(forecast_date__in=forecast_date_list)

        # Фильтр по дате
        if date_param is not None:
            from dateutil.parser import parse
            date_list = [parse(date_str).date() for date_str in date_param.split(",")]
            queryset = queryset.filter(sales_units__date__in=date_list)

        # Фильтр по спросу (target)
        if target_param is not None:
            target_list = target_param.split(",")
            queryset = queryset.filter(sales_units__target__in=target_list)
                
        return queryset
