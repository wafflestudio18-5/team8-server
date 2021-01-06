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
from podo_app.models import Profile, ProfileCity, City, Product
from user.serializer import UserAndProfileSerializer
from django.core.paginator import Paginator
#
from user.serializer import UserProductSerializer

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
                return Response({"error":"Oauth has not returned any data"}, status=status.HTTP_404_NOT_FOUND)
            try:
                username=social+"_"+str(token_response["sub"])
            except KeyError:
                return Response(token_response, status=status.HTTP_400_BAD_REQUEST)

        elif social=="Kakao":
            social_url="https://kapi.kakao.com/v2/user/me"
            authorization={"Authorization": "Bearer {ACCESS_TOKEN}".format(ACCESS_TOKEN=access_token)}        
            token_response = requests.get(
                social_url,
                headers=authorization
                )
            token_response=json.loads(token_response.text)

            if token_response==None:
                return Response({"error":"Oauth has not returned any data"}, status=status.HTTP_404_NOT_FOUND)
            try: 
                id=token_response["id"]
            except KeyError:
                error={"error":token_response["msg"]}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)       
            username=social+"_"+str(token_response["id"])
        else:
            return Response({"error":"'social' parameter is wrong"}, status=status.HTTP_400_BAD_REQUEST)

        is_new=not(User.objects.filter(username=username).exists())
                        
        if is_new:
            try:
                if social=="Google":
                    full_name=token_response["name"]
                elif social=="Kakao":
                    full_name=token_response["kakao_account"]["profile"]["nickname"]
            except KeyError:
                return Response({"error":"'full_name' is required"}, status=status.HTTP_404_NOT_FOUND)
            try:
                if social=="Google":
                    image=token_response["picture"]
                elif social=="Kakao":
                    image=token_response["properties"]["thumbnail"]
            except KeyError:
                image=None

            nickname=full_name
            
            user=User.objects.create_user(username)
            user.first_name=full_name
            user.save()
            profile=Profile.objects.create(user=user, nickname=nickname)
            if bool(image):
                profile.image=image

            profile.save()
            login(request, user)
        else:
            user=User.objects.get(username=username)
            login(request, user)
            profile=user.profile.get()
            full_name=user.first_name
            nickname=profile.nickname
            image=profile.image
            products_sold=profile.products_sold
            products_bought=profile.products_bought
        body={"user_id":user.id, "full_name":full_name, "nickname":nickname, 
            "products_bought":products_bought, "products_sold":products_sold, "temperature":profile.temperature}
        if bool(image):
            body["image"]=image        
        serializer=self.get_serializer(data=body)
        serializer.is_valid(raise_exception=True)
        data=serializer.data

        token, created=Token.objects.get_or_create(user=user)
        data["token"]=token.key

        if is_new:
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(data, status=status.HTTP_200_OK)
            


    @action(detail=False, methods=['POST'])
    def logout(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        logout(request)
        return Response(status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        if pk == 'me':
            user = request.user
        else :
            user=User.objects.get(id=pk)
        profile=user.profile.get()
        full_name=user.first_name
        nickname=profile.nickname
        image=profile.image
        products_sold=profile.products_sold
        products_bought=profile.products_bought

        body={"user_id":user.id, "full_name":full_name, "nickname":nickname, 
            "products_bought":products_bought, "products_sold":products_sold, "temperature":profile.temperature}
        if bool(image):
            body["image"]=image
        serializer=self.get_serializer(profile,data=body)
        serializer.is_valid(raise_exception=True)
        data=serializer.data
        return Response(data, status=status.HTTP_200_OK)
        
    def update(self, request, pk=None):
        if pk != 'me':
            return Response({"error": "Can't update other user's information"}, status=status.HTTP_403_FORBIDDEN)
        user = request.user
        profile=user.profile.get()
        if not user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        
        img = request.FILES.get('img-file')
        if img:
            profile.image=img
            profile.save()

        data=request.data
        try:
            data["full_name"]
            user.first_name=data["full_name"]
            user.save()
        except KeyError:
            pass

        serializer = self.get_serializer(profile, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data=serializer.data  
        return Response(data, status=status.HTTP_200_OK)



    def delete(self, request, pk=None):
        if pk != 'me':
            return Response({"error": "Can't update other Users information"}, status=status.HTTP_403_FORBIDDEN)
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user=request.user
        profile=request.user.profile.get()
        logout(request)
        user.delete()
        profile.delete()
        return Response(status=status.HTTP_200_OK)


    @action(detail=False, methods=['PUT', 'GET'])
    def city(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        user=request.user
        profile=user.profile.get()

        if request.method=="PUT":
            former_profilecities=ProfileCity.objects.filter(profile=profile)
            for i in former_profilecities:
                i.delete()

            city_id=[request.data["city_id_1"], request.data["city_id_2"]]
            body=[]
            for id in city_id:
                if id=="0":
                    pass
                else:   
                    try:
                        city=City.objects.get(id=id)
                    except City.DoesNotExist:
                        return Response({"error":"there is no city with the given id"}, status=status.HTTP_400_BAD_REQUEST)                
                    ProfileCity.objects.create(profile=profile, city=city)
                    body.append({"city_id":city.id, "city_name":city.name, "city_location":city.location})

            return Response({"user_id":user.id, "nickname":profile.nickname, "city": body}, status.HTTP_200_OK)
        
        elif request.method=="GET":
            cities=City.objects.filter()
            body=[]
            for city in cities:
                instance={"city_id": city.id, "city_name":city.name, "city_location":city.location}
                body.append(instance)
            
            return Response({"city":body}, status=status.HTTP_200_OK)

    @action(detail=False, methods=[ 'GET'])
    def productlist(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        user = request.user
        profile=user.profile.get()
        products=Product.objects.filter(seller=profile)#

        pages=Paginator(products, 10)
        try:
            page_number=request.data["page"]
            if not page_number.is_integer():
                return Response({"error": "'page' parameter is not integer"}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({"error": " 'page' parameter is not given"}, status=status.HTTP_400_BAD_REQUEST)
        p=pages.page(page_number)

        productbody=[]
        for product in products:
            product_serialized=UserProductSerializer(product)
            product_serialized.is_valid(raise_exception=True)
            productbody.append(product_serialized.data)

        pagebody={"product_count":pages.count, "page_count":pages.page_range[-1], "current_page":p.number}

        return Response({"page":pagebody, "product":productbody}, status=status.HTTP_200_OK)
        
    @action(detail=True, methods=[ 'GET'])
    def product(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        user = request.user
        profile=user.profile.get()
        try:
            product=Product.objects.get(seller=profile, id=pk)
        except Product.DoesNotExist:
            return Response({"error":"requested product does not exist"}, status=status.HTTP_404_NOT_FOUND)

        product_serialized=UserProductSerializer(product)  
        product_serialized.is_valid(raise_exception=True)
        data= product_serialized.data

        return Response(data, status=status.HTTP_200_OK)
