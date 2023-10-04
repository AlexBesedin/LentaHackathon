from rest_framework import serializers
from categories.models import Category
from stores.models import Store
from sales.models import Sales, SalesRecord
from django.shortcuts import get_object_or_404


class SalesRecordSerialazier(serializers.ModelSerializer):
    """Сериалайзер записи фактических исторических данных."""

    date = serializers.DateField()
    sales_type = serializers.IntegerField()
    sales_units = serializers.IntegerField()
    sales_units_promo = serializers.IntegerField()
    sales_rub = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    sales_rub_promo = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        model = SalesRecord
        fields = ('date',
                  'sales_type',
                  'sales_units',
                  'sales_units_promo',
                  'sales_rub',
                  'sales_rub_promo',)


class SalesSerializer(serializers.ModelSerializer):
    """Сериалайзер продаж. GET запрос"""
    store = serializers.SerializerMethodField()
    sku = serializers.SerializerMethodField()
    fact = SalesRecordSerialazier()

    class Meta:
        model = Sales
        fields = [
            'store',
            'sku',
            'fact',
        ]
        
    def get_store(self, obj):
        return str(obj.store)

    def get_sku(self, obj):
        return str(obj.sku)    


class CreateSalesSerializer(serializers.ModelSerializer):
    store = serializers.CharField()
    sku = serializers.CharField()
    fact = SalesRecordSerialazier()

    class Meta:
        model = Sales
        fields = [
            'store',
            'sku',
            'fact',
        ]
        
        
    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        internal_value['store'] = get_object_or_404(
            Store, 
            store__title=data['store']
        )
        internal_value['sku'] = get_object_or_404(
            Category, 
            sku=data['sku']
        )
        return internal_value


    def create(self, validated_data):
        fact_data = validated_data.pop('fact')
        fact_instance = SalesRecord.objects.create(**fact_data)
        sales_instance = Sales.objects.create(
            fact=fact_instance, 
            **validated_data
        )
        return sales_instance