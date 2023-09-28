from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from users.models import CustomUser
from django.contrib.auth import authenticate


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
               

class PasswordChangeSerializer(serializers.Serializer):
    """Сериализатор изменения пароля"""
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not authenticate(username=user.username, password=value):
            raise serializers.ValidationError('Старый пароль неверен.')
        return value

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
    

class PasswordResetSerializer(serializers.Serializer):
    """Сериализатор для сброса пароля"""
    username = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)

    def validate_username(self, value):
        try:
            user = CustomUser.objects.get(username=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(
                'Пользователь с таким именем пользователя не существует.'
            )
        return value

    def save(self):
        username = self.validated_data['username']
        user = CustomUser.objects.get(username=username)
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user

