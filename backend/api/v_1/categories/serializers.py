from categories.models import Category
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    group = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    subcategory = serializers.StringRelatedField()
    
    class Meta:
        model = Category
        fields = (
            'sku',
            'group',
            'category',
            'subcategory',
            'uom',
        )
