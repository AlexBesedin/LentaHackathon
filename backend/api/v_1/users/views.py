from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import MyUserCreateSerializer, SetSuperuserSerializer
from users.models import CustomUser


class CreateUserView(generics.CreateAPIView):
    """Вью для создания пользователя."""
    queryset = CustomUser.objects.all()
    serializer_class = MyUserCreateSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'user': MyUserCreateSerializer(user, context=self.get_serializer_context()).data,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SetSuperuserView(generics.GenericAPIView):
    """Назначит пользователя суперюзером"""
    serializer_class = SetSuperuserSerializer
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user_id = serializer.validated_data.get("id")
            username = serializer.validated_data.get("username")
            
            try:
                user = CustomUser.objects.get(id=user_id, username=username)
            except CustomUser.DoesNotExist:
                return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
            
            user.is_superuser = True
            user.save()
            
            return Response({"success": f"User {user.username} is now a superuser"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)