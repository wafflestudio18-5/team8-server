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
            'city',
            'buyer',
            'seller'
            'count_likes',
            'count_comments',
            'count_views',
        )
    def validate(self, data):
        name = data.get('name', None)
        category = data.get('category', None)
        price = data.get('price', None)
        allow_suggest = data.get('allow_suggest', None)
        city = data.get('city', None)
        seller = data.get('seller', None)

        if bool(name) ^ bool(category) ^ bool(price) ^ bool(allow_suggest) ^ bool(city) ^ bool(seller):
            raise serializers.ValidationError("not all required")
        return data



class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = (
            'id',
            'will_buyer',
            'is_active',
            'product',
        )

    def validate(self, data):
        will_buyer = data.get('will_buyer', None)
        product = data.get('product', None)

        if bool(will_buyer) ^ bool(product):
            raise serializers.ValidationError("not all required")
        return data


""" class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            'id',
            'ChatRoom_id',
            'body',
            'written_by',
        ) """

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
            'will_buyer',
            'confirm',
            'chatroom',
            'suggest_price'
        )

    def validate(self, data):
        will_buyer = data.get('will_buyer', None)
        chatroom = data.get('chatroom', None)
        suggest_price = data.get('suggest_price', None)

        if bool(will_buyer) ^ bool(chatroom) ^ bool(suggest_price):
            raise serializers.ValidationError("not all required")
        return data