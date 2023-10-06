from categories.models import Category, CategoryProduct, Group, Subcategory
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all()
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=CategoryProduct.objects.all()
    )
    subcategory = serializers.PrimaryKeyRelatedField(
        queryset=Subcategory.objects.all()
    )

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


class UniqueCategorySerializer(serializers.ModelSerializer):
    """Поиск уникальный категорий для фронта"""
    group = serializers.CharField(source='group.group')
    category = serializers.CharField(source='category.category')
    uom = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['group', 'category', 'uom']

    def get_uom(self, obj):
        return obj.get_uom_display()