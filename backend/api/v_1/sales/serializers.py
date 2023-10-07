from rest_framework import serializers
from categories.models import Category, CategoryProduct, Group
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
    
    fact = SalesRecordSerialazier(source='facts', many=True, read_only=True)
    store = serializers.SerializerMethodField()
    sku = serializers.SerializerMethodField()

    class Meta:
        model = Sales
        fields = [
            'store',
            'sku',
            'fact',
        ]

    def get_store(self, obj):
        """
        Метод возвращает заголовок магазина (захешированный ID магазина) 
        связанного с объектом продажи. Если по каким-то причинам название 
        магазина не может быть получено, метод возвращает None и печатает 
        сообщение об ошибке.
        """
        try:
            return str(obj.store.store.title)
        except AttributeError as e:
            print(f"Ошибка при получении магазина для объекта продаж {obj.id}: {str(e)}")
            return None 

    def get_sku(self, obj):
        """
        Метод возвращает SKU продукта связанного с объектом продажи.
        Если SKU не может быть получен, метод возвращает None.
        """
        if hasattr(obj, 'sku') and hasattr(obj.sku, 'sku'):
            return str(obj.sku.sku)
        return None  


class CreateSalesSerializer(serializers.ModelSerializer):
    """Сериалайзер продаж. POST запрос"""
    
    store = serializers.CharField()
    sku = serializers.CharField()
    facts = SalesRecordSerialazier(many=True)

    class Meta:
        model = Sales
        fields = [
            'store',
            'sku',
            'facts',
        ]
        
    def to_internal_value(self, data):
        """
        Метод преобразует входные данные API (обычно словарь) во внутреннее
        представление, проверяя наличие необходимых полей и преобразуя внешние
        ключи ('store' и 'sku') в соответствующие объекты модели.
        """
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
        """ 
        Метод создает экземпляр модели Sales, используя предоставленные
        проверенные данные. Вначале он извлекает данные facts из проверенных данных.
        Затем он пытается получить существующий экземпляр Sales с указанным 
        'store' и 'sku' или создать новый. После чего создает и связывает
        записи SalesRecord, если они предоставлены.
        """
        fact_data = validated_data.pop('facts', None)
        sales_instance, created = Sales.objects.get_or_create(
            store=validated_data['store'],
            sku=validated_data['sku']
        )
        if fact_data:
            fact_instances = []
            for fact in fact_data:
                fact_instance = SalesRecord.objects.create(**fact)
                fact_instances.append(fact_instance)
            sales_instance.facts.add(*fact_instances)
        else:
            raise serializers.ValidationError("Фактические данные отсутствуют или недостоверны")
        return sales_instance


class SalesCategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории для общего сериализатора продаж """
    
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all()
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=CategoryProduct.objects.all()
    )


    class Meta:
        model = Category
        fields = (
            'sku',
            'group',
            'category',
            'uom',
        )

    def to_representation(self, instance):
        """ 
        Метод преобразует экземпляр модели в словарь, который может быть
        использован для построения ответа API. Он добавляет дополнительные поля
        ('group' и 'category'), извлекая их из соответствующих связанных объектов,
        чтобы обеспечить более информативный ответ API.
        """
        representation = super().to_representation(instance)
        representation['group'] = instance.group.group
        representation['category'] = instance.category.category
        return representation
    
    
class CombinedSalesSerializer(serializers.ModelSerializer):
    """Общий сериализатор для продаж"""
    
    store = serializers.CharField(source='store.store.title')
    sku = serializers.CharField(source='sku.sku')
    group = serializers.CharField(source='sku.group.group')
    category = serializers.CharField(source='sku.category.category')
    uom = serializers.SerializerMethodField()
    fact = SalesRecordSerialazier(source='facts', many=True, read_only=True)

    class Meta:
        model = Sales
        fields = [
            'store', 
            'sku', 
            'group',
            'category', 
            'uom', 
            'fact',
        ]

    def get_uom(self, obj):
        return obj.sku.get_uom_display()