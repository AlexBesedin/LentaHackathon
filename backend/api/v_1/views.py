from api.serializers import StoreSerializer
from categories.models import Category
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from sales.models import Sale
from stores.models import Store


class StoreViewSet(viewsets.ReadOnlyModelViewSet):
    """Создаём вьюсет для магазинов."""

    queryset = Store.objects.all()
    serializer_class = StoreSerializer
