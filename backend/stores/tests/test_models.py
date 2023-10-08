from django.test import TestCase

from stores.models import Store, StoreID


class StoreIDModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.store_id = StoreID.objects.create(
            title='Пример хэш значение магазина',
        )

    def setUp(self):
        self.store_id = StoreIDModelTest.store_id

    def test_str_returns_title(self):
        """Проверяем, что у моделей корректно работает __str__."""
        self.assertEqual(str(self.store_id), 'Пример хэш значение магазина')

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        field_verboses = {
            "title": "захэшированное id магазина",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.store_id._meta.get_field(field).verbose_name, expected_value
                )


class StoreModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        store_id = StoreID.objects.create(title='захэшированное id магазина')
        cls.store = Store.objects.create(
            store=store_id,
            city='хэш города',
            division='хэш отдела',
            type_format=1,
            loc=2,
            size=3,
            is_active=1,
        )

    def setUp(self):
        self.store = StoreModelTest.store

    def test_str_returns_store_title(self):
        """Проверяем, что у моделей корректно работает __str__."""
        self.assertEqual(str(self.store), 'захэшированное id магазина')

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""

        field_verboses = {
            "store": "захэшированное id магазина",
            "city": "захэшированное id города",
            "division": "захэшированное id дивизиона",
            "type_format": "id формата магазина",
            "loc": "id тип локации/окружения магазина",
            "size": "id типа размера магазина",
            "is_active": "флаг активного магазина на данный момент",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.store._meta.get_field(field).verbose_name,
                    expected_value
                )
