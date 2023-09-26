# from api.v_1.views import (CategoryViewSet, Forecast_archiveViewSet, SaleViewSet,
#                        StoreViewSet)
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from api.v_1.users.views import CreateUserView, SetSuperuserView


app_name = 'api'

v1_router = DefaultRouter()

# v1_router.register('stores', StoreViewSet, basename='stores')
# v1_router.register('sales', SaleViewSet, basename='sales')
# v1_router.register('categories', CategoryViewSet, basename='categories')
# v1_router.register('forecast_archive', Forecast_archiveViewSet,
#                    basename='forecast_archive')


urlpatterns = [
    path('', include(v1_router.urls)),
    path('users/', CreateUserView.as_view(), name='user-create'),
    path('users/set_superuser/', SetSuperuserView.as_view(), name='set-superuser'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
