from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from podo_app.models import Profile


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = (
            'first_name',
        )

class UserAndProfileSerializer(serializers.ModelSerializer):
    user_id=serializers.IntegerField(required=True)
    full_name = serializers.CharField(required=False)
    nickname = serializers.CharField(required=False)
    image=serializers.URLField(required=False, allow_null=True)
    products_bought=serializers.IntegerField(required=False)    
    products_sold=serializers.IntegerField(required=False)    
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

        

    