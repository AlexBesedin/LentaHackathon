from datetime import datetime
from io import BytesIO

import pandas as pd
from django.http import Http404, HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import generics, mixins, status, views, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v_1.forecast.filters import ForecastFilterBackend
from api.v_1.forecast.serializers import StoreForecastSerializer
from api.v_1.utils.pagination import CustomPagination
from forecast.models import StoreForecast, UserBookmark

from .serializers import (StoreForecastCreateSerializer,
                          StoreForecastSerializer, UserBookmarkSerializer)


class StoreForecastViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = StoreForecast.objects.all()
    # permission_classes = [permissions.IsAdminUser]
    serializer_class = StoreForecastSerializer
    http_method_names = ['get', 'post']
    filter_backends = [ForecastFilterBackend]
    lookup_field = 'store__title'
    lookup_value_regex = '[^/]+'
    # pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return StoreForecastCreateSerializer
        return StoreForecastSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

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
            id=forecast_id,
        )
        if UserBookmark.objects.filter(
            user=user,
            store_forecast=forecast,
        ).exists():
            return Response(
                {'detail': 'Предсказание уже добавлено'},
                status=status.HTTP_400_BAD_REQUEST)
        bookmark = UserBookmark.objects.create(
            user=user,
            store_forecast=forecast,
        )
        serializer = UserBookmarkSerializer(bookmark)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class RemoveFromBookmarksView(views.APIView):
    """Удаляем предсказание из избранного"""

    def delete(self, request, bookmark_id, *args, **kwargs):
        user = request.user
        bookmark = get_object_or_404(
            UserBookmark,
            id=bookmark_id,
            user=user,
        )
        bookmark.delete()
        return Response(
            {'detail': 'Удалено из закладок.'},
            status=status.HTTP_204_NO_CONTENT)


class UserBookmarksView(generics.ListAPIView):
    """Отображает список добавленого в избранное"""

    serializer_class = UserBookmarkSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = UserBookmark.objects.filter(user=user)
        return queryset


class SaveForecastExcelView(APIView):
    """Функция сохранения прогноза в excel."""

    def get(self, request, store_hash):
        """Получение и сохранение предсказаний для конкретного магазина"""

        forecasts = get_list_or_404(
            StoreForecast, 
            store__store__title=store_hash)
        forecast_data = [StoreForecastSerializer(forecast).data for
                         forecast in forecasts]
        store_name = forecasts[0].store.store.title if forecasts else "неизвестный магазин"
        df = pd.DataFrame(forecast_data)

        df.rename(columns={
            'store': 'Магазин',
            'sku': 'Артикул',
            'forecast_date': 'Дата прогноза',
            'forecast': 'Прогноз'
        }, inplace=True)

        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        output.seek(0)
        current_date = datetime.now().strftime("%Y-%m-%d")
        filename = f"{store_name}_forecast_{current_date}.xlsx"
        response = HttpResponse(output.read(),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'
        return response
