from rest_framework import serializers
from sales.models import SalesRecord, Sales

class SalesRecordSerializer(serializers.ModelSerializer):
    """Сериализато для чтения исторических данных продаж"""
    
    class Meta:
        model = SalesRecord
        fields = [
            'date',
            'sales_type',
            'sales_units',
            'sales_units_promo',
            'sales_rub',
            'sales_rub_promo',
            ]
        

class SalesRecordWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для входящих исторических данных продаж
    на запись в бд"""
    class Meta:
        model = SalesRecord
        fields = [
            'date',
            'sales_type',
            'sales_units',
            'sales_units_promo',
            'sales_rub',
            'sales_rub_promo',
        ]        
        

class SalesSerializer(serializers.ModelSerializer):
    """Сериализатор продаж"""
    fact = SalesRecordSerializer(
        source='sales_records', 
        many=True, 
        read_only=True
    )
    sales_records = SalesRecordWriteSerializer(
        many=True, 
        write_only=True, 
        required=False
    )
    
    class Meta:
        model = Sales
        fields = [
            'store', 
            'sku', 
            'fact', 
            'sales_records'
        ]
        
    def create(self, validated_data):
        sales_records_data = validated_data.pop('sales_records', [])
        sales = Sales.objects.create(**validated_data)
        for sales_record_data in sales_records_data:
            SalesRecord.objects.create(fact=sales, **sales_record_data)
        return sales
        
        
