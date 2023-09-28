import json

from django.http import JsonResponse
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from stores.models import Store

from .serializers import StoreSerializer


class StoreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Store.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = StoreSerializer
    http_method_names = ['get']

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
