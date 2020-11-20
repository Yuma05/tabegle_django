from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from api.models import UserShop, Shop
from api.serializer import UserShopSerializer
from rest_framework import status

class UserShopList(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserShopSerializer

    def get_queryset(self):
        queryset = UserShop.objects.get(user=self.request.user)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


class UserShopChange(APIView):
    permission_classes = (IsAuthenticated, )

    def put(self, request, pk, format=None):
        queryset = UserShop.objects.get(user=self.request.user)
        try:
            add_shop = Shop.objects.get(id=pk)
        except Shop.DoesNotExist:
            return Response({'message': 'Incorrect shop ID.'}, status=status.HTTP_400_BAD_REQUEST)
        queryset.shops.add(add_shop)
        serializer = UserShopSerializer(queryset)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        queryset = UserShop.objects.get(user=self.request.user)
        try:
            delete_shop = Shop.objects.get(id=pk)
        except Shop.DoesNotExist:
            return Response({'message': 'Incorrect shop ID.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            UserShop.objects.get(shops=delete_shop)
        except UserShop.DoesNotExist:
            return Response({'message': 'The shop is not registered.'}, status=status.HTTP_400_BAD_REQUEST)
        queryset.shops.remove(delete_shop)
        serializer = UserShopSerializer(queryset)
        return Response(serializer.data)
