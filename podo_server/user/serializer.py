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
    
class LikeProductSerializer(serializers.ModelSerializer):
    active = serializers.BooleanField(default=True)
    class Meta:
        model = LikeProduct
        fields = (
            'id',
            'profile',
            'product',
            'active',
        )

    def validate(self, data):
        profile = data.get('profile', None)
        product = data.get('product', None)

        if not (bool(profile) and bool(product)):
            raise serializers.ValidationError("not all required")
        return data

class LikeProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeProduct
        fields = (
            'id',
            'profile',
            'product',
            'active'
        )
