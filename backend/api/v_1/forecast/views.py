from rest_framework import permissions, viewsets, response, status
from api.v_1.forecast.serializers import StoreForecastSerializer
from forecast.models import StoreForecast


class ForecastViewSet(viewsets.ModelViewSet):
    """
    list:
    Возвращает список всех прогнозов.
    
    retrieve:
    Возвращает конкретный прогноз по id.
    
    create:
    Создает новый прогноз.
    """
    queryset = StoreForecast.objects.all()
    serializer_class = StoreForecastSerializer
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ['get', 'post']
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = []
        for store_forecast_representation in serializer.data:
            data.extend(store_forecast_representation)
        return response.Response({'data': data})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return response.Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(
                serializer.data, 
                status=status.HTTP_201_CREATED
            )
        return response.Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )
    