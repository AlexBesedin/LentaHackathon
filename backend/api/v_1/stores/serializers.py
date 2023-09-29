from rest_framework import serializers
from stores.models import Store, StoreID


class StoreIDSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = StoreID 
        fields = ['title']  
        
        
class StoreSerializer(serializers.ModelSerializer):
    store = StoreIDSerializer()

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