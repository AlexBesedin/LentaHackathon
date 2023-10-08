from api.v_1.categories.serializers import (CategorySerializer,
                                            UniqueCategorySerializer)
from categories.models import Category, CategoryProduct, Group, Subcategory
from django.test import TestCase


class CategorySerializerTestCase(TestCase):
    def setUp(self):
        self.group = Group.objects.create(group='Test Group')
        self.category = CategoryProduct.objects.create(category='Test Category')
        self.subcategory = Subcategory.objects.create(subcategory='Test Subcategory')
        self.category_instance = Category.objects.create(
            sku='test_sku',
            group=self.group,
            category=self.category,
            subcategory=self.subcategory,
            uom='test_uom'
        )

    def test_to_representation(self):
        """Проверяем формат правильность формата данных."""

        serializer = CategorySerializer(instance=self.category_instance)
        serialized_data = serializer.data
        expected_data = {
            'sku': 'test_sku',
            'group': 'Test Group',
            'category': 'Test Category',
            'subcategory': 'Test Subcategory',
            'uom': 'test_uom'
        }
        self.assertEqual(serialized_data, expected_data)


class UniqueCategorySerializerTestCase(TestCase):
    def setUp(self):
        self.group = Group.objects.create(group='Test Group')
        self.category = CategoryProduct.objects.create(category='Test Category')
        self.category_instance = Category.objects.create(
            group=self.group,
            category=self.category,
            uom='test_uom'
        )

    def test_get_uom(self):
        """Проверяем формат правильность формата данных."""

        serializer = UniqueCategorySerializer(instance=self.category_instance)
        uon_value = serializer.get_uom(self.category_instance)
        self.assertEqual(uon_value, 'test_uom')
