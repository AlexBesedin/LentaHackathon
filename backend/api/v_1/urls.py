from api.v_1.categories.views import CategoryViewSet
from api.v_1.sales.views import SalesViewSet
from api.v_1.stores.views import StoreViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v_1.forecast.views import StoreForecastAPIView
from api.v_1.users.views import LoginWithCodeView, PasswordResetRequestView


app_name = 'api'

v1_router = DefaultRouter()

v1_router.register('shops', StoreViewSet, basename='shops')
v1_router.register('sales', SalesViewSet, basename='sales')
v1_router.register('categories', CategoryViewSet, basename='categories')


urlpatterns = [
    path('', include(v1_router.urls)),
    path('users/reset-password/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('users/login-with-code/', LoginWithCodeView.as_view(), name='login-with-code'),
    path('forecast/', StoreForecastAPIView.as_view(), name='forecast'),
    path(r'auth/', include('djoser.urls.authtoken'))
]
