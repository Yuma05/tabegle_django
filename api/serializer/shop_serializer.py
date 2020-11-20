from rest_framework import serializers

from api.models import Shop


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = (
            'id', 'name', 'img_src', 'url', 'address', 'tabelog_rating', 'tabelog_review_num', 'google_rating',
            'google_review_num', 'total_rating'
        )
