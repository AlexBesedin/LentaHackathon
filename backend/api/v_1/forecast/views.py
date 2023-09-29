from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework.generics import ListCreateAPIView

from forecast.models import StoreForecast
from .serializers import StoreForecastSerializer, StoreForecastCreateSerializer


class StoreForecastAPIView(ListCreateAPIView):
    queryset = StoreForecast.objects.all()
    permission_classes = [permissions.IsAdminUser]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return StoreForecastCreateSerializer
        return StoreForecastSerializer


    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data})
    
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, 
            many=isinstance(
                request.data, list)
            )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED
        )

 