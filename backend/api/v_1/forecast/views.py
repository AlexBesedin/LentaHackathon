import pandas as pd

from rest_framework.response import Response
from rest_framework import status, viewsets, views, generics
from django.shortcuts import get_object_or_404

from forecast.models import StoreForecast, UserBookmark
from .serializers import (
    StoreForecastSerializer, 
    StoreForecastCreateSerializer, 
    UserBookmarkSerializer
    )


class StoreForecastViewSet(viewsets.ModelViewSet):
    queryset = StoreForecast.objects.all()
    # permission_classes = [permissions.IsAdminUser]
    serializer_class = StoreForecastSerializer
    http_method_names = ['get', 'post']
    lookup_field = 'store'

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return StoreForecastCreateSerializer
        return StoreForecastSerializer
    
    
    # def write_data_to_excel(data_list, file_path):
    #     """Функция записи данных прогноза в excel-файл."""

    #     df = pd.DataFrame(data_list)
    #     writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
    #     df.to_excel(writer, index=False)
    #     writer.save()


    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        data_list = response.data
        # file_path = 'data.xlsx'
        # self.write_data_to_excel(data_list)
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


class AddToBookmarksView(views.APIView):
    """Добавляем предсказание в избранное"""
    
    def post(self, request, forecast_id, *args, **kwargs):
        user = request.user
        forecast = get_object_or_404(
            StoreForecast, 
            id=forecast_id
        )
        if UserBookmark.objects.filter(
            user=user, 
            store_forecast=forecast
            ).exists():
            return Response(
                {'detail': 'Предсказание уже добавлено'}, status=status.HTTP_400_BAD_REQUEST)
        bookmark = UserBookmark.objects.create(
            user=user, 
            store_forecast=forecast
        )
        serializer = UserBookmarkSerializer(bookmark)
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED
        )


class RemoveFromBookmarksView(views.APIView):
    """Удаляем предсказание из избранного"""
    
    def delete(self, request, bookmark_id, *args, **kwargs):
        user = request.user
        bookmark = get_object_or_404(
            UserBookmark, 
            id=bookmark_id, 
            user=user
        )
        bookmark.delete()
        return Response(
            {'detail': 'Удалено из закладок.'}, status=status.HTTP_204_NO_CONTENT)


class UserBookmarksView(generics.ListAPIView):
    """Отображает список добавленого в избранное"""
    serializer_class = UserBookmarkSerializer
    
    def get_queryset(self):
        user = self.request.user
        queryset = UserBookmark.objects.filter(user=user)
        return queryset