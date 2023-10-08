from rest_framework import serializers

from stores.models import Store, StoreID


class StoreIDSerializer(serializers.ModelSerializer):
    """Сериализатор ID магазинов."""

    class Meta:
        model = StoreID
        fields = '__all__'


class StoreSerializer(serializers.ModelSerializer):
    """Сериализатор для магазинов."""

    # store = StoreIDSerializer()
    store = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = [
            'store',
            'city',
            'division',
            'type_format',
            'loc',
            'size',
            'is_active',
        ]

    def get_store(self, obj):
        return str(obj.store)

    def get_is_active(self, obj):
        return 'Активный' if obj.is_active else 'Неактивный'
