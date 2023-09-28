from rest_framework import serializers
from stores.models import Store


class StoreSerializer(serializers.ModelSerializer):

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
