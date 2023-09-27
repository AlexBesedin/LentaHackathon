from api.v_1.sales.serializers import StoreSerializer
from rest_framework import permissions, response, viewsets
from rest_framework.decorators import action
from stores.models import Store


@action(detail=True, methods=['get'])
class StoreViewSet(viewsets.ReadOnlyModelViewSet):
    """Создаём вьюсет для магазинов."""

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAdminUser]

    def list(self, request, *args, **kwargs):
        """
        Переопределенный метод для GET запроса на получение списка объектов Store
        """
        queryset = self.get_queryset()
        serializer = StoreSerializer(queryset, many=True)
        return response.Response(serializer.data)
