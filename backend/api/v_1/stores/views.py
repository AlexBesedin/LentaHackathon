from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.response import Response

from api.v_1.stores.filters import StoreFilter
from stores.models import Store

from .serializers import StoreSerializer

# from api.v_1.utils.pagination import CustomPagination


class StoreViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет магазинов."""

    queryset = Store.objects.all()
    # permission_classes = [permissions.IsAdminUser]
    serializer_class = StoreSerializer
    http_method_names = ['get']
    lookup_field = 'store'
    filter_backends = [DjangoFilterBackend]
    filterset_class = StoreFilter
    # filterset_fields = [
    #     'store__title',
    #     'city',
    #     'division',
    #     'type_format',
    #     'loc',
    #     'size',
    #     'is_active',
    # ]
    ordering_fields = '__all__'
    # pagination_class = CustomPagination

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
        """Функция отображения списка магазинов."""

        # queryset = self.get_queryset()
        # page = self.paginate_queryset(queryset)
        # serializer = self.get_serializer(page, many=True)
        # return self.get_paginated_response(serializer.data)
        queryset = self.filter_queryset(self.get_queryset())
        serializer = StoreSerializer(queryset, many=True)
        return Response(serializer.data)
