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