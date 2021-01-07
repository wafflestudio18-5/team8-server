from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from podo_app.models import Profile

class UserAndProfileSerializer(serializers.ModelSerializer):
    user_id=serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    nickname = serializers.CharField()
    image=serializers.SerializerMethodField()
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
    def get_user_id(self, profile):
        return profile.user.id
    def get_image(self, profile):
        if profile.image:
            return profile.image
        else:
            return profile.image_url
    
