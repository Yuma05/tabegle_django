from rest_framework import serializers

from api.models import UserShop
from api.serializer import ShopSerializer


class UserShopSerializer(serializers.ModelSerializer):
    shops = ShopSerializer(many=True)

    class Meta:
        model = UserShop
        fields = ('user', 'shops')
