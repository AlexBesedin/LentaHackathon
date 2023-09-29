import json

from api.v_1.stores.filters import StoreFilter
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from stores.models import Store

from .serializers import StoreSerializer


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = StoreSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    lookup_field = 'store'
    filter_backends = [DjangoFilterBackend]
    filterset_class = StoreFilter
    filterset_fields = [
        'store__title', 
        'city', 
        'division', 
        'type_format',
        'loc', 
        'size', 
        'is_active',
    ]
    ordering_fields = '__all__'

    def get_queryset(self):
        queryset = Store.objects.all()
        
        filter_fields = [
            'store__title', 
            'city', 
            'division', 
            'type_format',
            'loc', 
            'size', 
            'is_active',
        ]
        
        filters = {}
        for field in filter_fields:
            value = self.request.query_params.get(field, None)
            if value is not None:
                filters[field] = value
        
        return queryset.filter(**filters)


    def list(self, request, *args, **kwargs):
        """Функция отображения списко магазинов."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        return Response({'data': data})


    def load_stores(request):
        """Функция загрузки исторических данных по магазинам."""
        data = request.POST.get('data')
        if data:
            try:
                json_data = json.loads(data)
                for item in json_data['data']:
                    store_name = item['store']
                    city = item['city']
                    division = item['division']
                    type_format = item['type_format']
                    loc = item['loc']
                    size = item['size']
                    is_active = bool(item['is_active'])
                    Store.objects.create(
                        store=store_name,
                        city=city,
                        division=division,
                        type_format=type_format,
                        loc=loc,
                        size=size,
                        is_active=is_active
                    )
                return JsonResponse({'status': 'success'})
            except (json.JSONDecodeError, KeyError, ValueError):
                return JsonResponse({'error': 'Неверный формат данных.'})

        else:
            return JsonResponse({'error': 'Данные не были предоставлены.'})
