from rest_framework import generics, status
from rest_framework.response import Response

from django.core.mail import send_mail

from .serializers import (LoginWithCodeSerializer,
                          PasswordResetRequestSerializer,)
from api.v_1.users.utils import generate_random_code
from users.models import CustomUser


class PasswordResetRequestView(generics.CreateAPIView):
    """Представление для обработки запроса на сброс пароля."""
    serializer_class = PasswordResetRequestSerializer

    def create(self, request, *args, **kwargs):
        """Обработка POST запроса для сброса пароля."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user = CustomUser.objects.get(email=email)
        temp_password = generate_random_code(8)
        user.set_password(temp_password)
        user.save()

        subject = "Сброс пароля"
        plain_message = f"Ваш временный код: {temp_password}"
        html_message = f"""
        <h1>Сброс пароля</h1>
        <p>Вы запросили сброс пароля на нашем сайте.</p>
        <p><b>Ваш временный код: {temp_password}</b></p>
        <p>Если вы не запрашивали сброс пароля, проигнорируйте это письмо.</p>
        """

        send_mail(
            subject,
            plain_message,
            'from_email@gmail.com',
            [email],
            html_message=html_message,
            fail_silently=False,
        )

        return Response(
            {"detail": "Код отправлен на ваш email."}, status=status.HTTP_200_OK)


class LoginWithCodeView(generics.CreateAPIView):
    """Представление для обработки запроса на вход с использованием кода."""
    serializer_class = LoginWithCodeSerializer

    def create(self, request, *args, **kwargs):
        """Обработка POST запроса для входа с использованием кода."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"detail": "Успешный вход."}, status=status.HTTP_200_OK)
