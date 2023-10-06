from api.v_1.categories.views import CategoryViewSet, UniqueSubcategoryView
from api.v_1.forecast.views import StoreForecastViewSet, UserBookmarksView
from api.v_1.sales.views import SalesViewSet
from api.v_1.stores.views import StoreViewSet
from api.v_1.users.views import LoginWithCodeView, PasswordResetRequestView
from django.test import TestCase
from django.urls import resolve, reverse


class UrlsTest(TestCase):
    def test_categories_list_url(self):
        """Тестируем путь в списку категорий."""

        url = reverse('api:categories-list')
        self.assertEqual(resolve(url).func.cls, CategoryViewSet)

    def test_sales_list_url(self):
        """Тестируем путь в списку продаж."""

        url = reverse('api:sales-list')
        self.assertEqual(resolve(url).func.cls, SalesViewSet)

    def test_stores_list_url(self):
        """Тестируем путь в списку магазинов."""

        url = reverse('api:shops-list')
        self.assertEqual(resolve(url).func.cls, StoreViewSet)

    def test_forecast_list_url(self):
        """Тестируем путь в списку прознозных значений."""

        url = reverse('api:forecast-list')
        self.assertEqual(resolve(url).func.cls, StoreForecastViewSet)

    def test_password_reset_request_url(self):
        """Тестируем путь для переустановки пароля для регистрации."""

        url = reverse('api:password-reset-request')
        self.assertEqual(resolve(url).func.view_class, PasswordResetRequestView)

    def test_login_with_code_url(self):
        """Тестируем путь для логина в систему с помощью кода."""

        url = reverse('api:login-with-code')
        self.assertEqual(resolve(url).func.view_class, LoginWithCodeView)

    def test_user_bookmarks_url(self):
        """Тестируем путь к user_bookmarks."""

        url = reverse('api:user_bookmarks')
        self.assertEqual(resolve(url).func.view_class, UserBookmarksView)

    def test_unique_categories_url(self):
        """Тестируем путь к unique-categories."""

        url = reverse('api:unique-categories')
        self.assertEqual(resolve(url).func.view_class, UniqueSubcategoryView)
