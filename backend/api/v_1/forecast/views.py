import pandas as pd
from api.v_1.forecast.filters import ForecastFilterBackend
from api.v_1.utils.pagination import CustomPagination
from django.shortcuts import get_object_or_404
from forecast.models import StoreForecast, UserBookmark
from rest_framework import generics, status, views, viewsets
from rest_framework.response import Response

from .serializers import (StoreForecastCreateSerializer,
                          StoreForecastSerializer, UserBookmarkSerializer)


class StoreForecastViewSet(viewsets.ModelViewSet):
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
