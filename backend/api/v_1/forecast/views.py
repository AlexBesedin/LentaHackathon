import pandas as pd

from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.generics import ListCreateAPIView

from forecast.models import StoreForecast
from .serializers import StoreForecastSerializer, StoreForecastCreateSerializer


class StoreForecastAPIView(ListCreateAPIView):
    queryset = StoreForecast.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = StoreForecastSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return StoreForecastCreateSerializer
        return StoreForecastSerializer
    
    
    def write_data_to_excel(data_list, file_path):
        """Функция записи данных прогноза в excel-файл."""

        df = pd.DataFrame(data_list)
        writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
        df.to_excel(writer, index=False)
        writer.save()


    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        data_list = response.data
        file_path = 'data.xlsx'
        self.write_data_to_excel(data_list, file_path)
        return Response({'data': response.data})
    
    
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
