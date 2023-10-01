from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .serializers import PasswordChangeSerializer, PasswordResetSerializer


class ChangePasswordView(generics.GenericAPIView):
    """Изменить пароль"""
    serializer_class = PasswordChangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {'detail': 'Пароль успешно обновлен'}, 
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
            )


class ResetPasswordView(generics.GenericAPIView):
    """Сбросить пароль"""
    serializer_class = PasswordResetSerializer
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {'detail': 'Пароль успешно сброшен'}, 
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
            )

