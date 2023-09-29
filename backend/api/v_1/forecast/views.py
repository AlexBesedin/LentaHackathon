# from forecast.models import StoreForecast
# from rest_framework import mixins, viewsets
# from rest_framework.response import Response

# from .serializers import StoreForecastSerializer


# class StoreForecastViewSet(mixins.RetrieveModelMixin,
#                            mixins.ListModelMixin,
#                            viewsets.GenericViewSet):
#     """
#     ViewSet для обработки GET запросов.
#     """
#     queryset = StoreForecast.objects.all()
#     serializer_class = StoreForecastSerializer

#     def list(self, request, *args, **kwargs):
#         response = super().list(request, *args, **kwargs)
#         return Response({'data': response.data})


import pandas as pd
from forecast.models import StoreForecast
from rest_framework import mixins, viewsets
from rest_framework.response import Response

from .serializers import StoreForecastSerializer


class StoreForecastViewSet(mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    """
    ViewSet для обработки GET запросов.
    """
    queryset = StoreForecast.objects.all()
    serializer_class = StoreForecastSerializer

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
