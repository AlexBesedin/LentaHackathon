from rest_framework import serializers
from sales.models import Sales, SalesRecord
from stores.models import Store
from categories.models import Category


class SalesRecordSerialazier(serializers.ModelSerializer):
    class Meta:
        model = SalesRecord
        fields = '__all__'


class SalesSerializer(serializers.ModelSerializer):
    fact = SalesRecordSerialazier()
    store = serializers.SlugRelatedField(slug_field='store', queryset=Store.objects.all())
    sku = serializers.SlugRelatedField(slug_field='sku', queryset=Category.objects.all())

    class Meta:
        model = Sales
        fields = ('store', 'sku', 'fact',)

    def create(self, validated_data):
        fact_data = validated_data.pop('fact')
        fact = SalesRecord.objects.create(**fact_data)
        store_slug = validated_data.pop('store')
        sku_slug = validated_data.pop('sku')
        store = Store.objects.get(store=store_slug)
        sku = Category.objects.get(sku=sku_slug)
        
        return Sales.objects.create(fact=fact, store=store, sku=sku, **validated_data)
