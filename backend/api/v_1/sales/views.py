from rest_framework import permissions, viewsets, response
from sales.models import Sales
from api.v_1.sales.serializers import SalesSerializer
from rest_framework.decorators import action


@action(detail=True, methods=['get'])
class SalesViewSet(viewsets.ModelViewSet):
    """Viewset для объектов модели Sales"""
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def list(self, request, *args, **kwargs):
        """
        Переопределенный метод для GET запроса на получение списка объектов Sales
        """
        queryset = self.get_queryset()
        serializer = SalesSerializer(queryset, many=True)
        return response.Response(serializer.data)