from rest_framework import serializers

from api.models import Place


class PlaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Place
        fields = ('name', 'kana', 'place_code')
