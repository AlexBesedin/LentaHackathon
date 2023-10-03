from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from .serializers import CategorySerializer
from api.v_1.categories.filters import CategoryFilter
from categories.models import Category


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
    pagination_class = None

    # def get_queryset(self):
    #     """
    #     Этот метод получает все объекты Category и фильтрует их 
    #     на основе параметров запроса.
    #     """
    #     queryset = Category.objects.all()
    #     filter_fields = ['sku', 'group__group', 'category__category', 'subcategory__subcategory']
    #     filters = {}
    #     for field in filter_fields:
    #         value = self.request.query_params.get(field, None)
    #         if value is not None:
    #             filters[field] = value 
    #     return queryset.filter(**filters)

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


    def get_categories(request):
        """Функция получения исторических данных по категориям."""

        categories = Category.objects.all()
        data = []
        for category in categories:
            data.append({
                'sku': category.sku,
                'group': category.group.group,
                'category': category.category,
                'subcategory': category.subcategory.subcategory,
                'uom': category.uom
            })
        return JsonResponse({'data': data})
