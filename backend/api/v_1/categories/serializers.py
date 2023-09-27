from categories.models import Category
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'sku',
            'group',
            'category',
            'subcategory',
            'uom',
        )
