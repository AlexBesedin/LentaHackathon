from rest_framework import permissions, viewsets
from rest_framework.response import Response
from stores.models import Store

from .serializers import StoreSerializer


class StoreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Store.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = StoreSerializer
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        return Response({'data': data})
