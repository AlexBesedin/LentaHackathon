from rest_framework import serializers
from forecast.models import StoreForecast, DailySalesForecast
from stores.models import Store
from categories.models import Category
from datetime import datetime


class DailySalesForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailySalesForecast
        fields = ['date', 'target']


class StoreForecastSerializer(serializers.ModelSerializer):
    """ДЛЯ ГЕТ"""
    store = serializers.CharField(source='store.store')
    sku = serializers.CharField(source='sku.sku')
    forecast = serializers.SerializerMethodField()

    class Meta:
        model = StoreForecast
        fields = ['store', 'sku', 'forecast_date', 'forecast']

    def get_forecast(self, obj):
        forecasts = DailySalesForecast.objects.filter(forecast_sku_id=obj).order_by('date')
        return {forecast.date.strftime('%Y-%m-%d'): forecast.target for forecast in forecasts}
