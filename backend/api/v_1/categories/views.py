from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from api.v_1.categories.filters import CategoryFilter
from api.v_1.utils.pagination import CustomPagination
from categories.models import Category

from .serializers import CategorySerializer, UniqueCategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет для товарной иерархии."""

    queryset = Category.objects.all()
    # permission_classes = [permissions.IsAdminUser]
    serializer_class = CategorySerializer
    http_method_names = ['get']
    lookup_field = 'sku'
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter
    ordering_fields = '__all__'
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        """Функция отображения списка категорий"""

        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Функция добавления категорий товаров"""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    # def get_categories(request):
    #     """Функция получения исторических данных по категориям."""

    #     categories = Category.objects.all()
    #     data = []
    #     for category in categories:
    #         data.append({
    #             'sku': category.sku,
    #             'group': category.group.group,
    #             'category': category.category,
    #             'subcategory': category.subcategory.subcategory,
    #             'uom': category.uom
    #         })
    #     return JsonResponse({'data': data})


class UniqueSubcategoryView(ListAPIView):
    """Дополнительная логика для отображения уникальных categories"""

    serializer_class = UniqueCategorySerializer

    def get_queryset(self):
        unique_category_ids = Category.objects.values('category').annotate(min_id=models.Min('id')).values('min_id')
        return Category.objects.filter(id__in=unique_category_ids)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
