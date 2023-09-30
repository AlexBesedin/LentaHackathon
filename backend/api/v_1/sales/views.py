import json
from datetime import datetime

from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from rest_framework import permissions, viewsets
from rest_framework.response import Response

from api.v_1.sales.serializers import CreateSalesSerializer, SalesSerializer
from sales.models import Sales, SalesRecord
from .filters import SalesFilter


class SalesViewSet(viewsets.ModelViewSet):
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer  
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ['get', 'post']
    lookup_field = 'store'
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_class = SalesFilter
    
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateSalesSerializer
        return SalesSerializer

    
    def create(self, request, *args, **kwargs):
        """Функция создания категории."""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)


    def list(self, request, *args, **kwargs):
        """Переопределенный метод для GET запроса
        на получение списка объектов Sales."""

        queryset = self.get_queryset()
        serializer = SalesSerializer(queryset, many=True)
        return Response(serializer.data)


    def get_sales(request):
        """Функция получения исторических данных по продажам."""

        data = request.POST.get('data')
        if data:
            try:
                json_data = json.loads(data)
                sales_data = []
                for item in json_data['data']:
                    store = item['store']
                    sku = item['sku']
                    sales_records = item['fact']
                    sales, _ = Sales.objects.get_or_create(
                        store=store,
                        sku=sku,
                    )
                    for record in sales_records:
                        date_str = record['date']
                        date = datetime.strptime(date_str, '%Y-%m-%d').date()
                        sales_type = record['sales_type']
                        sales_units = record['sales_units']
                        sales_units_promo = record['sales_units_promo']
                        sales_rub = record['sales_rub']
                        sales_run_promo = record['sales_run_promo']
                        SalesRecord.objects.create(
                            fact=sales,
                            date=date,
                            sales_type=sales_type,
                            sales_units=sales_units,
                            promo_units=sales_units_promo,
                            sales_rub=sales_rub,
                            promo_rub=sales_run_promo
                        )
                    sales_data.append({
                        'store': store,
                        'sku': sku,
                        'fact': sales_records,
                    })
                return JsonResponse({'data': sales_data})      
            except (json.JSONDecodeError, KeyError, ValueError):
                return JsonResponse({'error': 'Неверный формат данных.'})
        else:
            return JsonResponse({'error': 'Данные не предоставлены.'})
