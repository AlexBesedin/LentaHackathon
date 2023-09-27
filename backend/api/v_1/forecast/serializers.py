from rest_framework import serializers
from forecast.models import StoreForecast, SkuForecast, DailySalesForecast
from collections import OrderedDict

class DailySalesForecastSerializer(serializers.ModelSerializer):
    """Сериализатор для модели DailySalesForecast."""
    class Meta:
        model = DailySalesForecast
        fields = ['date', 'target']


class SkuForecastSerializer(serializers.ModelSerializer):
    """Сериализатор для модели SkuForecast. Cериализатор также включает
    связанные экземпляры DailySalesForecast через поле `sales_units`."""
    sales_units = DailySalesForecastSerializer(
        many=True, 
        read_only=True, 
        source='dailysalesforecast_set'
    )
    sku = serializers.SerializerMethodField()
    
    class Meta:
        model = SkuForecast
        fields = ['sku', 'sales_units']


    def get_sku(self, obj):
        """Получить значение sku из связанного объекта."""
        return obj.sku.sku

    def to_representation(self, instance):
        """Настройка представления сериализованных данных. Поле sales_units
        преобразуется в словарь с датой как ключом и target как значением."""
        representation = super().to_representation(instance)
        forecast_representation = OrderedDict()
        for sales_unit in representation['sales_units']:
            forecast_representation[sales_unit['date']] = sales_unit['target']
        return {
            'sku': representation['sku'],
            'forecast': forecast_representation,
        }

    def create(self, validated_data):
        """Настроенный метод создания для обработки создания связанных 
        экземпляров DailySalesForecast."""
        sales_units_data = validated_data.pop('sales_units')
        sku_forecast = SkuForecast.objects.create(**validated_data)
        for sales_units_data_item in sales_units_data:
            DailySalesForecast.objects.create(
                sales_units=sku_forecast, 
                **sales_units_data_item
            )
        return sku_forecast


class StoreForecastSerializer(serializers.ModelSerializer):
    """Сериализатор для модели StoreForecast. Этот сериализатор включает
    связанные экземпляры SkuForecast через поле `sku_forecasts`."""
    sku_forecasts = SkuForecastSerializer(many=True)

    class Meta:
        model = StoreForecast
        fields = ['store', 'forecast_date', 'sku_forecasts']

    def to_representation(self, instance):
        """Настройка представления сериализованных данных. Каждый экземпляр SkuForecast
        добавляется в список с дополнительными полями store и forecast_date."""
        representation = super().to_representation(instance)
        sku_forecasts_representation = []
        for sku_forecast in representation['sku_forecasts']:
            sku_forecast_representation = {
                'store': representation['store'],
                'sku': sku_forecast['sku'],
                'forecast_date': representation['forecast_date'],
                'forecast': sku_forecast['forecast'],
            }
            sku_forecasts_representation.append(sku_forecast_representation)
        return sku_forecasts_representation
