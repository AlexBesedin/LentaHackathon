from api.v_1.categories.views import CategoryViewSet
from api.v_1.sales.views import SalesViewSet
from api.v_1.stores.views import StoreViewSet
from api.v_1.users.views import ChangePasswordView, ResetPasswordView
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v_1.forecast.views import StoreForecastAPIView


app_name = 'api'

v1_router = DefaultRouter()

v1_router.register('shops', StoreViewSet, basename='shops')
v1_router.register('sales', SalesViewSet, basename='sales')
v1_router.register('categories', CategoryViewSet, basename='categories')


urlpatterns = [
    path('', include(v1_router.urls)),
    path('users/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('users/reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('forecast/', StoreForecastAPIView.as_view(), name='forecast'),
    path(r'auth/', include('djoser.urls.authtoken'))
]
