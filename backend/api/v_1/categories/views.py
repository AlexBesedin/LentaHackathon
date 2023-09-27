from categories.models import Category
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from .serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет для товарной иерархии."""

    queryset = Category.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = CategorySerializer
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        """Функция добавления категорий товаров."""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )
