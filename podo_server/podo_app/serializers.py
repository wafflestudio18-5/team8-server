from rest_framework import serializers
from podo_app.models import Product, LikeProduct, ChatRoom, Transaction, SuggestPrice

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

        if not (bool(name) and bool(category) and bool(price) and bool(allow_suggest) and bool(city) and bool(seller)):
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

        if not(bool(will_buyer) and bool(product)):
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

        if not(bool(will_buyer) and bool(chatroom) and bool(suggest_price)):
            raise serializers.ValidationError("not all required")
        return data