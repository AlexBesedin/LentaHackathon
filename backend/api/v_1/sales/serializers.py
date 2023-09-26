from rest_framework import serializers
from sales.models import SalesRecord, Sales

class SalesRecordSerializer(serializers.ModelSerializer):
    
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
    fact = SalesRecordSerializer(source='sales_records', many=True, read_only=True)
    
    class Meta:
        model = Sales
        fields = ['store', 'sku', 'fact']
