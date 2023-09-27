from rest_framework import permissions, viewsets, response, status
from sales.models import Sales
from api.v_1.sales.serializers import SalesSerializer


class SalesViewSet(viewsets.ModelViewSet):
    """Viewset для объектов модели Sales"""
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ['get', 'post']
    
    def create(self, request, *args, **kwargs):
        """
        Переопределенный метод для POST запроса на создание объекта Sales
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(
            serializer.data, 
            status=status.HTTP_201_CREATED, 
            headers=headers
        )
    
    
    def list(self, request, *args, **kwargs):
        """
        Переопределенный метод для GET запроса на получение списка объектов Sales
        """
        queryset = self.get_queryset()
        serializer = SalesSerializer(queryset, many=True)
        return response.Response(serializer.data)