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
    def validate(self, attrs):
        return

class LikeProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeProduct
        fields = (
            'id',
            'profile_id',
            'product_id',
        )

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = (
            'id',
            'product_id',
            'body',
            'buyer_id',
        )

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            'id',
            'ChatRoom_id',
            'body',
            'written_by',
        )

class AppointmentSerializer(serializers.ModelSerializer):
    time = serializers.TimeField(format='%H:%H', input_formats=['%H:%H'])
    class Meta:
        model = Appointment
        fields = (
            'id',
            'seller_id',
            'buyer_id',
            'product_id',
            'confirm',
            'chatroom_id',
            'time'
        )

class SuggestPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuggestPrice
        fields = (
            'id',
            'seller_id',
            'buyer_id',
            'product_id',
            'confirm',
            'chatroom_id',
            'suggest_price'
        )