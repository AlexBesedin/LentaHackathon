from categories.filters import CategoryFilter
from categories.models import Category
from rest_framework import permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import CategorySerializer


from rest_framework import viewsets, permissions
from categories.models import Category
from .serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет для товарной иерархии."""
    
    queryset = Category.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = CategorySerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    lookup_field = 'sku'
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter
    filterset_fields = ['sku', 'group', 'category', 'subcategory']
    ordering_fields = '__all__'

