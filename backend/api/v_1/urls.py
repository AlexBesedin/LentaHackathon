from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v_1.categories.views import CategoryViewSet, UniqueSubcategoryView
from api.v_1.forecast.views import (AddToBookmarksView,
                                    RemoveFromBookmarksView,
                                    SaveForecastExcelView,
                                    StoreForecastViewSet, UserBookmarksView)
from api.v_1.sales.views import (AddToSalesBookmarksView,
                                 RemoveFromSalesBookmarksView,
                                 SalesDetailViewSet, SalesViewSet,
                                 UserSalesBookmarksView)
from api.v_1.stores.views import StoreViewSet
from api.v_1.users.views import LoginWithCodeView, PasswordResetRequestView

app_name = 'api'

v1_router = DefaultRouter()

v1_router.register('shops', StoreViewSet, basename='shops')
v1_router.register('sales', SalesViewSet, basename='sales')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('forecast', StoreForecastViewSet, basename='forecast')
v1_router.register('detail-sales', SalesDetailViewSet, basename='detail-sales')


urlpatterns = [
    path('', include(v1_router.urls)),
    path('users/reset-password/', PasswordResetRequestView.as_view(),
         name='password-reset-request'),
    path('users/login-with-code/', LoginWithCodeView.as_view(),
         name='login-with-code'),
    path('forecast/bookmarks_add/<int:forecast_id>/',
         AddToBookmarksView.as_view(), name='add_to_bookmarks'),
    path('forecast/bookmarks_remove/<int:bookmark_id>/',
         RemoveFromBookmarksView.as_view(), name='remove_from_bookmarks'),
    path('forecast/bookmarks/', UserBookmarksView.as_view(),
         name='user_bookmarks'),
    path('unique-categories/', UniqueSubcategoryView.as_view(),
         name='unique-categories'),
    path('auth/', include('djoser.urls.authtoken')),
    path('forecast/save_to_excel/<store_hash>/',
         SaveForecastExcelView.as_view(), name='save_forecast_excel'),
    path('sales/bookmarks_add/<int:sales_id>/',
         AddToSalesBookmarksView.as_view(), name='add_to_salesbookmarks'),
    path('sales/bookmarks_remove/<int:salesbookmark_id>/',
         RemoveFromSalesBookmarksView.as_view(),
         name='remove_from_salesbookmarks'),
    path('sales/bookmarks/', UserSalesBookmarksView.as_view(),
         name='user_salesbookmarks'),
]
