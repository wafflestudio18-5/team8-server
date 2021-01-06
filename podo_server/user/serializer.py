from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from podo_app.models import Profile
#
from podo_app.models import Product, LikeProduct, ChatRoom, Message

class UserAndProfileSerializer(serializers.ModelSerializer):
    user_id=serializers.IntegerField()
    full_name = serializers.SerializerMethodField()
    nickname = serializers.CharField()
    image=serializers.ImageField(required=False, allow_null=True)
    products_bought=serializers.IntegerField()    
    products_sold=serializers.IntegerField()
    temperature=serializers.FloatField()
    class Meta:
        model=Profile
        fields=(
            "user_id",
            "full_name",
            "nickname", 
            "image", 
            "temperature",
            "products_bought",
            "products_sold"
        )
        
    def get_full_name(self, profile):
        return profile.user.first_name

    

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