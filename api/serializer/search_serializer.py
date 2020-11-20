from rest_framework import serializers

from api.models import Search

from api.serializer import ShopSerializer


class SearchSerializer(serializers.ModelSerializer):
    shops = ShopSerializer(many=True)

    class Meta:
        model = Search
        fields = ('place_code', 'category_code', 'shops')
