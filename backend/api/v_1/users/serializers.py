from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from users.models import CustomUser


class MyUserCreateSerializer(UserCreateSerializer):
    """ Сериализатор создания пользователя. """
    class Meta:
        model = CustomUser 
        fields = (
            'email', 
            'username', 
            'first_name', 
            'last_name', 
            'password'
            )
        extra_kwargs = {'password': {'write_only': True}}
        

class SetSuperuserSerializer(serializers.Serializer):
    """Сериализатор отображения полей для назначениия
    суперюзера"""
    id = serializers.IntegerField()
    username = serializers.CharField()
    
    class Meta:
        model = CustomUser
      