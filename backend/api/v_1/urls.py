from api.views import (CategoryViewSet, Forecast_archiveViewSet, SaleViewSet,
                       StoreViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

v1_router = DefaultRouter()
v1_router.register('stores', StoreViewSet, basename='stores')
v1_router.register('sales', SaleViewSet, basename='sales')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('forecast_archive', Forecast_archiveViewSet,
                   basename='forecast_archive')


urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
