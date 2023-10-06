from categories.models import CategoryProduct, Group, Subcategory
from django.test import TestCase


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group_id = Group.objects.create(
            group='Пример захэшированной группы товара',
        )

    def setUp(self):
        self.group_id = GroupModelTest.group_id

    def test_str_returns_group_id(self):
        """Проверяем, что у моделей корректно работает __str__."""
        self.assertEqual(str(self.group_id), 'Пример захэшированной группы товара')

    def test_verbose_name_in_Group(self):
        """verbose_name в полях совпадает с ожидаемым."""

        field_verboses = {
            "group": "захэшированная группа товара",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.group_id._meta.get_field(field).verbose_name, expected_value
                )


class CategoryProductModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        group_id = Group.objects.create(group='захэшированная группа товара')
        cls.group = CategoryProduct.objects.create(
            group=group_id,
            category='захэшированная группа товара',
        )

    def setUp(self):
        self.group = CategoryProductModelTest.group

    def test_str_returns_group(self):
        """Проверяем, что у моделей корректно работает str."""

        self.assertEqual(str(self.group), 'захэшированная группа товара')

    def test_verbose_name_in_CategoryProduct(self):
        """verbose_name в полях совпадает с ожидаемым."""

        field_verboses = {
            'group': 'захэшированная группа товара',
            'category': 'захэшированная категория товара',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.group._meta.get_field(field).verbose_name, expected_value
                )


# class SubcategoryModelTest(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         category_id = CategoryProduct.objects.create(category='захэшированная категория товара')
#         cls.subcategory = Subcategory.objects.create(
#             category=category_id,
#             subcategory='захэшированная подкатегория товара',
#         )

#     def setUp(self):
#         self.category = SubcategoryModelTest.category

#     def test_str_returns_category(self):
#         """Проверяем, что у моделей корректно работает str."""
#         self.assertEqual(str(self.category), 'захэшированная категория товара')

#     def test_verbose_name_in_Subcategory(self):
#         """verbose_name в полях совпадает с ожидаемым."""

#         field_verboses = {
#             'subcategory': 'захэшированная подкатегория товара',
#             'category': 'захэшированная категория товара',
#         }
#         for field, expected_value in field_verboses.items():
#             with self.subTest(field=field):
#                 self.assertEqual(
#                     self.subcategory._meta.get_field(field).verbose_name, expected_value
#                 )
