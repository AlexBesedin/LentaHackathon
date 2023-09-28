from rest_framework import mixins, viewsets
from rest_framework.response import Response
from forecast.models import StoreForecast
from .serializers import StoreForecastSerializer


class StoreForecastViewSet(mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    """
    ViewSet для обработки GET запросов.
    """
    queryset = StoreForecast.objects.all()
    serializer_class = StoreForecastSerializer
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({'data': response.data})