import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
import user.models as usermodel
from django.db import models
import requests
from podo_app.models import Profile
from user.serializer import UserandProfileSerializer
import random 

class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserandProfileSerializer
    permission_classes = (IsAuthenticated(), )

    def get_permissions(self):
        if self.action in ('create', 'login', 'update'):
            return (AllowAny(), )
        return self.permission_classes

    def create(self, request):
        access_token=request.data['access_token']
        social_url=""
        social=request.data['social']
#change to google
        if social=="Github":
            social_url="https://api.github.com/user"
            authorization={"Authorization": "Bearer {ACCESS_TOKEN}".format(ACCESS_TOKEN=access_token)}
        elif social=="Kakao":
            social_url="https://kapi.kakao.com/v2/user/me"
            authorization={"Authorization": "Bearer {ACCESS_TOKEN}".format(ACCESS_TOKEN=access_token)}
        
        token_response = requests.get(
            social_url,
            headers=authorization
            )
        token_response=json.loads(token_response.text)

        if token_response==None:
            return Response("Oauth has not returned any data", status=status.HTTP_404_NOT_FOUND)
        username=social+"_"+str(token_response["id"])

        new=False
        try:
            user=User.objects.get(username=username)
        except User.DoesNotExist:
            new=True

        if new:
            try:
                full_name=token_response["kakao_account"]["profile"]["nickname"]
            except KeyError:
                return Response("full_name is required", status=status.HTTP_400_BAD_REQUEST)
#img check
            try:
                image=token_response["properties"]["thumbnail"]
            except KeyError:
                image=None

            try:
                nickname=request.data["nickname"]
            except KeyError:
                nickname=full_name

            user=User.objects.create_user(username)
#change if possible
            user.first_name=full_name
            user.save()
            profile=Profile.objects.create(user=user, nickname=nickname, image=image)
            profile.save()
            login(request, user)
        else:
            login(request, user)
            full_name=user.first_name
            nickname=user.profile.get().nickname

        body={"user_id":user.id, "full_name":full_name, "nickname":nickname}
        serializer=self.get_serializer(data=body)
        serializer.is_valid(raise_exception=True)
        data=serializer.data
        data['token']=user.auth_token.key

        if new:
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(data, status=status.HTTP_200_OK)
            


    @action(detail=False, methods=['POST'])
    def logout(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
