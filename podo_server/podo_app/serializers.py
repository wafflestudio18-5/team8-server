from rest_framework import serializers
from podo_app.models import Product, LikeProduct, ChatRoom, Transaction, SuggestPrice
from user.serializer import LikeProductSerializer

class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    likeproduct = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'category',
            'price',
            'body',
            'status',
            'distance_range',
            'city',
            'allow_suggest',
            'buyer',
            'seller',
            'count_likes',
            'count_comments',
            'count_views',
            'images',
            'likeproduct',
        )

    def validate(self, data):
        name = data.get('name', None)
        category = data.get('category', None)
        price = data.get('price', None)
        allow_suggest = data.get('allow_suggest', None)
        city = data.get('city', None)
        seller = self.context['request'].user
        if not (bool(name) and bool(category) and bool(price) and bool(allow_suggest) and bool(city)):
            raise serializers.ValidationError("not all required")
        return data
    
    def get_images(self, product):
        product_image_list = list(product.images.all())
        return map( lambda product_image: {"id":product_image.id,"image_url":product_image.image.url} ,product_image_list)

    def get_likeproduct(self, product):
        query = LikeProduct.objects.filter(product = product)
        return LikeProductSerializer(query, many=True).data



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
            'product',
            'suggest_price'
        )

    def validate(self, data):
        will_buyer = data.get('will_buyer', None)
        suggest_price = data.get('suggest_price', None)

        if not(bool(will_buyer) and bool(suggest_price)):
            raise serializers.ValidationError("not all required")
        return data