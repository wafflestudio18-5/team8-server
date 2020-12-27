from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from podo_app.models import Profile


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
#add this to design
    last_login = serializers.DateTimeField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_login',
            'date_joined',
        )

class ProfileSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(required=False)
#add this to design
    image = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Profile
        fields = (
            'nickname',
            'image',
        )

class UserAndProfileSerializer(serializers.ModelSerializer):
    user_id=serializers.IntegerField(required=True)
    full_name = serializers.CharField(required=False)
    nickname = serializers.CharField(required=False)
    image=serializers.URLField(required=False, allow_null=True)
    class Meta:
        model=Profile
        fields=(
            "user_id",
            "full_name",
            "nickname", 
            "image", 
            "temperature",
#            "badges",
#            "Products bought",
#            "Products sold",
        )

#    def 


    