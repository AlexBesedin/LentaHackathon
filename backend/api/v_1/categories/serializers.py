from categories.models import Category, CategoryProduct, Group, Subcategory
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=CategoryProduct.objects.all())
    subcategory = serializers.PrimaryKeyRelatedField(queryset=Subcategory.objects.all())

    class Meta:
        model = Category
        fields = (
            'sku',
            'group',
            'category',
            'subcategory',
            'uom',
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['group'] = instance.group.group
        representation['category'] = instance.category.category
        representation['subcategory'] = instance.subcategory.subcategory
        return representation
