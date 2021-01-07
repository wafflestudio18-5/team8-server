from rest_framework import serializers
from ..podo_app.models import Product, LikeProduct, ChatRoom, Message

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'category',
            'price',
            'status',
            'distance_range',
            'city_id',
            'buyer_id',
            'seller_id'
            'count_likes',
            'count_comments',
            'count_views',
        )