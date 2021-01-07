from rest_framework import serializers
from ..podo_app.models import Product, LikeProduct, ChatRoom, Transaction

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


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            'id',
            'chatroom',
            'buyer_review',
            'seller_review'
        )
    
    def validate(self, data):
        chatroom = data.get('chatroom', None)
        if bool(chatroom):
            raise serializers.ValidationError("not all required")
        return data

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