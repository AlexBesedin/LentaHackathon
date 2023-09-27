from api.v_1.categories.views import CategoryViewSet
from api.v_1.sales.views import SalesViewSet
from api.v_1.stores.views import StoreViewSet
from api.v_1.users.views import CreateUserView, SetSuperuserView
from api.v_1.forecast.views import ForecastViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

app_name = 'api'

v1_router = DefaultRouter()

v1_router.register('shops', StoreViewSet, basename='shops')
v1_router.register('sales', SalesViewSet, basename='sales')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('forecast', ForecastViewSet, basename='forecast')


urlpatterns = [
    path('', include(v1_router.urls)),
    path('users/', CreateUserView.as_view(), name='user-create'),
    path('users/set_superuser/', SetSuperuserView.as_view(), name='set-superuser'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
