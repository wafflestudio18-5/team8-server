from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from podo_app.models import Profile
#
from podo_app.models import Product, LikeProduct, ChatRoom, Message

class UserAndProfileSerializer(serializers.ModelSerializer):
    id=serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    nickname = serializers.CharField()
    image=serializers.SerializerMethodField()
    products_bought=serializers.IntegerField()    
    products_sold=serializers.IntegerField()
    temperature=serializers.FloatField()
    class Meta:
        model=Profile
        fields=(
            "id",
            "full_name",
            "nickname", 
            "image", 
            "temperature",
            "products_bought",
            "products_sold"
        )
        
    def get_full_name(self, profile):
        return profile.user.first_name
    def get_id(self, profile):
        return profile.user.id
    def get_image(self, profile):
        if profile.image:
            return profile.image.url
        else:
            return profile.image_url
    

class UserProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'category',
            'price',
            'status',
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
            'profile',
            'product',
            'active'
        )
