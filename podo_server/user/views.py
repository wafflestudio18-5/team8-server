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
from podo_app.models import Profile, ProfileCity, City
from user.serializer import UserAndProfileSerializer, ProfileSerializer, UserSerializer

class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserAndProfileSerializer
    permission_classes = (IsAuthenticated(), )

    def get_permissions(self):
        if self.action in ('create', 'login', 'update'):
            return (AllowAny(), )
        return self.permission_classes

    def create(self, request):
        access_token=request.data['access_token']
        social_url=""
        social=request.data['social']
        if social=="Google":
            social_url="https://oauth2.googleapis.com/tokeninfo?id_token={ACCESS_TOKEN}".format(ACCESS_TOKEN=access_token)
            token_response = requests.get(
                social_url
                )
            token_response=json.loads(token_response.text)
            if token_response==None:
                return Response("Oauth has not returned any data", status=status.HTTP_404_NOT_FOUND)
            username=social+"_"+str(token_response["sub"])



        elif social=="Kakao":
            social_url="https://kapi.kakao.com/v2/user/me"
            authorization={"Authorization": "Bearer {ACCESS_TOKEN}".format(ACCESS_TOKEN=access_token)}        
            token_response = requests.get(
                social_url,
                headers=authorization
                )
            token_response=json.loads(token_response.text)
            username=social+"_"+str(token_response["id"])


        new=False
        try:
            user=User.objects.get(username=username)
        except User.DoesNotExist:
            new=True
                
#        return Response(user.profile.get().id)        
        
        if new:
            try:
                if social=="Google":
                    full_name=token_response["name"]
                elif social=="Kakao":
                    full_name=token_response["kakao_account"]["profile"]["nickname"]
            except KeyError:
                return Response("full_name is required", status=status.HTTP_400_BAD_REQUEST)
            try:
                if social=="Google":
                    image=token_response["picture"]
                elif social=="Kakao":
                    image=token_response["properties"]["thumbnail"]
            except KeyError:
                image=None

            try:
                nickname=request.data["nickname"]
            except KeyError:
                nickname=full_name
            
            user=User.objects.create_user(username)
            user.first_name=full_name
            user.save()
            profile=Profile.objects.create(user=user, nickname=nickname)
            if image!=None:
                profile.image=image

            profile.save()
            login(request, user)
        else:
            login(request, user)
            profile=user.profile.get()
            full_name=user.first_name
            nickname=profile.nickname
            image=profile.image
        body={"user_id":user.id, "full_name":full_name, "nickname":nickname}
        if image!="":
            body["image"]=image
        serializer=self.get_serializer(data=body)
        serializer.is_valid(raise_exception=True)
        data=serializer.data

        if new:
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(data, status=status.HTTP_200_OK)
            


    @action(detail=False, methods=['POST'])
    def logout(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        user=User.objects.get(id=pk)
        profile=user.profile.get()
        full_name=user.first_name
        nickname=profile.nickname
        image=profile.image
        body={"user_id":user.id, "full_name":full_name, "nickname":nickname}
        if image!=None:
            body["image"]=image
        serializer=self.get_serializer(data=body)
        serializer.is_valid(raise_exception=True)
        data=serializer.data
        return Response(data, status=status.HTTP_200_OK)
        


    def update(self, request, pk=None):
        if pk != 'me':
            return Response({"error": "Can't update other Users information"}, status=status.HTTP_403_FORBIDDEN)
        user = request.user
        if not user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        ####more        
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        data=serializer.data  
        return Response(data, status=status.HTTP_200_OK)



    def delete(self, request, pk=None):
        if pk != 'me':
            return Response({"error": "Can't update other Users information"}, status=status.HTTP_403_FORBIDDEN)

        user=request.user
        profile=request.user.profile.get()
        logout(request)
        user.delete()
        profile.delete()
        return Response(status=status.HTTP_200_OK)


    @action(detail=False, methods=['POST', 'PUT',  'DEL'])
    def city(self, request):
        user=request.user
        profile=user.profile.get()
        city_id=request.data["city_id"]
        city=City.objects.get(id=city_id)
        if request.method=="POST":
            profilecity=ProfileCity.create(profile=profile, city=city)

            body={"nickname":profile.nickname, "city":[]}
            profilecities=profilecity.filter(profile=profile)
            for i in profilecities:
                city=i.city
                body["city"].append({"city_name":city.name, "city_location":city.location}) 
            return Response(body, status.HTTP_201_CREATED)

        elif request.method=="PUT":
            former_city_id=request.data["former_city_id"]
            former_city=City.objects.get(id=former_city_id)
            profilecity=ProfileCity.objects.get(profile=profile, city=former_city)
            profilecity.city=city

            body={"nickname":profile.nickname, "city":[]}
            profilecities=profilecity.filter(profile=profile)
            for i in profilecities:
                city=i.city
                body["city"].append({"city_name":city.name, "city_location":city.location}) 
            return Response(body, status.HTTP_200_OK)
        
        elif request.method=="DEL":
            profilecity=ProfileCity.objects.get(profile=profile, city=city)
            profilecity.delete()

            body={"nickname":profile.nickname, "city":[]}
            profilecities=profilecity.filter(profile=profile)
            for i in profilecities:
                city=i.city
                body["city"].append({"city_name":city.name, "city_location":city.location}) 
            return Response(body, status.HTTP_200_OK)

