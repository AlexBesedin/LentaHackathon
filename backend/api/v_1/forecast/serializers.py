from rest_framework import serializers
from django.core.exceptions import ValidationError

from categories.models import Category
from stores.models import Store
from forecast.models import StoreForecast, DailySalesForecast, UserBookmark


class DailySalesForecastSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DailySalesForecast
        fields = [
            'date', 
            'target'
        ]


class StoreForecastSerializer(serializers.ModelSerializer):
    """Сериализатор для GET запроса"""
    store = serializers.CharField(source='store.store')
    sku = serializers.CharField(source='sku.sku')
    forecast = serializers.SerializerMethodField()

    class Meta:
        model = StoreForecast
        fields = [
            'store', 
            'sku', 
            'forecast_date', 
            'forecast'
        ]

    def get_forecast(self, obj):
        forecasts = DailySalesForecast.objects.filter(forecast_sku_id=obj).order_by('date')
        return {forecast.date.strftime('%Y-%m-%d'): forecast.target for forecast in forecasts}
    

class StoreForecastCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для POST запроса"""
    store = serializers.CharField()
    sku = serializers.CharField()
    sales_units = DailySalesForecastSerializer(many=True)

    class Meta:
        model = StoreForecast
        fields = [
            'store',  
            'sku',
            'forecast_date',
            'sales_units'
        ]

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        try:
            internal_value['store'] = Store.objects.get(store__title=data['store'])
        except Store.DoesNotExist:
            raise ValidationError(
                {"store": "Магазин с таким названием не существует."}
            )
        try:
            internal_value['sku'] = Category.objects.get(sku=data['sku'])
        except Category.DoesNotExist:
            raise ValidationError(
                {"sku": "Категория с таким артикулом не существует."}
            )
        return internal_value

    def create(self, validated_data):
        sales_units_data = validated_data.pop('sales_units')
        store_forecast = StoreForecast.objects.create(**validated_data)
        for sales_unit_data in sales_units_data:
            DailySalesForecast.objects.create(
                forecast_sku_id=store_forecast, 
                **sales_unit_data
            )
        return store_forecast


class UserBookmarkSerializer(serializers.ModelSerializer):
    """Сериализатор избранных предсказаний"""
    
    class Meta:
        model = UserBookmark
        fields = [
            'id', 
            'user', 
            'store_forecast', 
            'created_at'
        ]
        
        
class UserBookmarkSerializer(serializers.ModelSerializer):
    """Сериализатор отображения избранного"""
    
    store_forecast = StoreForecastSerializer(read_only=True)

    class Meta:
        model = UserBookmark
        fields = [
            'id', 
            'store_forecast', 
            'created_at'
        ]