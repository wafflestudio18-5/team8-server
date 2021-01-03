from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from podo_app.models import Profile

class UserAndProfileSerializer(serializers.ModelSerializer):
    user_id=serializers.IntegerField()
    full_name = serializers.CharField()
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
            "products_sold",
#            "badges",
        )
        

    
