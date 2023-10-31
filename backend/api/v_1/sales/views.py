from django.shortcuts import get_object_or_404

from rest_framework import (generics, mixins, status, views,
                            viewsets)
from rest_framework.response import Response

from api.v_1.sales.filters import SaleFilterBackend, SalesDetailBackend
from api.v_1.sales.serializers import (CombinedSalesSerializer,
                                       CreateSalesSerializer, SalesSerializer,
                                       UserSalesBookmarkSerializer)
from api.v_1.utils.pagination import CustomPagination
from sales.models import Sales, UserSalesBookmark


class SalesViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    http_method_names = ['get', 'post']
    lookup_field = 'store'
    pagination_class = CustomPagination
    filter_backends = [SaleFilterBackend]

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
        """Переопределенный метод для GET запроса на получение списка объектов Sales."""

        queryset = self.filter_queryset(self.get_queryset().order_by('id'))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = SalesSerializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)

class SalesDetailViewSet(viewsets.ModelViewSet):
    """Детали продажи detail-sales"""

    queryset = Sales.objects.all()
    serializer_class = CombinedSalesSerializer
    http_method_names = ['get', ]
    filter_backends = [SalesDetailBackend]

    def list(self, request, *args, **kwargs):
        """Переопределенный метод для GET запроса
        на получение списка объектов Sales."""

        queryset = self.filter_queryset(self.get_queryset())
        serializer = CombinedSalesSerializer(queryset, many=True)
        return Response(serializer.data)


class AddToSalesBookmarksView(views.APIView):
    """Добавляем данные по продажам в избранное"""

    def post(self, request, sales_id, *args, **kwargs):
        user = request.user
        sales = get_object_or_404(
            Sales,
            id=sales_id,
        )
        if UserSalesBookmark.objects.filter(
            user=user,
            sales=sales,
        ).exists():
            return Response(
                {'detail': 'Данные по продажам уже добавлены в избранное.'},
                status=status.HTTP_400_BAD_REQUEST)
        salesbookmark = UserSalesBookmark.objects.create(
            user=user,
            sales=sales,
        )
        serializer = UserSalesBookmarkSerializer(salesbookmark)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class RemoveFromSalesBookmarksView(views.APIView):
    """Удаляем данные по продажам из избранного"""

    def delete(self, request, salesbookmark_id, *args, **kwargs):
        user = request.user
        salesbookmark = get_object_or_404(
            UserSalesBookmark,
            id=salesbookmark_id,
            user=user,
        )
        salesbookmark.delete()
        return Response(
            {'detail': 'Удалено из закладок.'},
            status=status.HTTP_204_NO_CONTENT)


class UserSalesBookmarksView(generics.ListAPIView):
    """Отображает список добавленого в избранное"""

    serializer_class = UserSalesBookmarkSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = UserSalesBookmark.objects.filter(user=user)
        return queryset
