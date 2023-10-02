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


class PasswordResetRequestSerializer(serializers.Serializer):
    """Сериализатор для обработки запроса на сброс пароля."""
    email = serializers.EmailField()

    def validate_email(self, value):
        """Проверка существования пользователя с указанным email."""
        try:
            user = CustomUser.objects.get(email=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(
                "Пользователь с таким email не найден."
            )
        return value


class LoginWithCodeSerializer(serializers.Serializer):
    """Сериализатор для обработки запроса на вход с помощью кода."""
    email = serializers.EmailField()
    code = serializers.CharField()

    def validate(self, data):
        """Проверка корректности email и кода."""
        try:
            user = CustomUser.objects.get(email=data["email"])
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(
                "Пользователь с таким email не найден."
                )
        if not user.check_password(data["code"]):
            raise serializers.ValidationError(
                "Неверный код."
                )
        return data
