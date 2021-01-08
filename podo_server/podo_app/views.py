from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.paginator import Paginator
from podo_app.models import *
from podo_app.serializers import *

class ProductViewSet(viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ('create', 'delete'):
            return super(ProductViewSet, self).get_permissions()
        return (IsAuthenticated(), )

    def get_serializer_class(self):
        return self.serializer_class

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        
        img = request.FILES.get('img-file')
        if img:
            product_image = ProductImage.objects.create(product=product)
            product_image.image = img
            product_image.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        product = self.get_object()
        return Response(self.get_serializer(product).data)

    def list(self, request):
        name = request.query_params.get('name')
        order = request.query_params.get('order')
        max_price = request.query_params.get('max_price')
        category = request.query_params.get('category')
        city = request.query_params.get('city')
        products = self.get_queryset()
        if name:
            products = products.filter(name__icontains=name)
        if order == 'earliest':
            products = products.order_by('created_at')
        else:
            products = products.order_by('-created_at')
        if max_price:
            products = products.filter(price__lte=max_price)  ## max_price 보다 작은 것
        if category:
            products = products.filter(category=category)
        if city:
            products = products.filter(city=city)

        pages = Paginator(products, 10)
        if not request.data.get("page", None):
            return Response({"error": "no page parameter"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            page_number = request.data.get("page")
        if not float(page_number).is_integer():
            return Response({"error": "page para is not int"}, status=status.HTTP_400_BAD_REQUEST)
        p=pages.page(page_number)

        p_list=[]
        for i in products:
            product_serialized=ProductSerializer(i)
            p_list.append(product_serialized.data)

        pagebody={"product_count":pages.count, "page_count":pages.page_range[-1], "current_page":p.number}

        return Response({"page":pagebody, "product":p_list}, status=status.HTTP_200_OK)
        



        return Response(self.get_serializer(products, many=True).data)

    def delete(self, request, pk=None):
        product = self.get_object()
        product.delete()
        return Response(self.get_serializer(product).data, status=status.HTTP_200_OK)


    @action(detail=True, methods=['PUT', 'POST', 'DELETE'])
    def suggestprice(self, request, pk):
        product = self.get_object()
        if self.request.method == 'POST':
            return self._suggest_price(product)
        elif self.request.method == 'PUT':
            return self._confirm_price(product)
        else:
            return self._deny_price(product)

    def _suggest_price(self, product):
        if not product.allow_suggest:
            return Response({"error": "now allowed"}, status=status.HTTP_403_FORBIDDEN)
        
        user = Profile.objects.get(user=self.request.user)
        if product.seller == user:
            return Response({"error": "you are seller!"}, status=status.HTTP_403_FORBIDDEN)

        serializer = SuggestPriceSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        price = serializer.save()
        price.product=product
        price.save()
        serializer = SuggestPriceSerializer(price)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _confirm_price(self, product):
        user = Profile.objects.get(user=self.request.user)
        if not product.seller == user:
            return Response({"error": "you are not seller!"}, status=status.HTTP_403_FORBIDDEN)
        suggestion = product.suggest_prices.get()
        suggestion.confirm = True
        suggestion.save()

        return Response(SuggestPriceSerializer(suggestion).data, status=status.HTTP_200_OK)

    def _deny_price(self, product):
        user = Profile.objects.get(user=self.request.user)
        if not product.seller == user:
            return Response({"error": "you are not seller!"}, status=status.HTTP_403_FORBIDDEN)
        suggestion = product.suggest_prices.get()
        suggestion.delete()
        return Response(SuggestPriceSerializer(suggestion).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def image(self, request, pk=None):
        product = self.get_object()
        
        img = request.FILES.get('img-file')
        if img:
            product_image = ProductImage.objects.create(product=product)
            product_image.image = img
            product_image.save()
        
        return Response(self.get_serializer(product).data, status=status.HTTP_201_CREATED)

    @image.mapping.delete
    def deleteImage(self, request, pk=None):
        img_id = request.data.get('id',None)
        if img_id:
            if ProductImage.objects.filter(id=img_id).exists():
                ProductImage.objects.get(id=img_id).delete()
        product = self.get_object()
        return Response(self.get_serializer(product).data, status=status.HTTP_200_OK)

class ChatRoomViewSet(viewsets.GenericViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        return super(ChatRoomViewSet, self).get_permissions()

    def get_serializer_class(self):
        return self.serializer_class

    def create(self, request):
        if ChatRoom.objects.filter(will_buyer=request.data.get('will_buyer', None), product=request.data.get('product', None)).exists(): 
            return Response({"error": "You have already chatroom"}, status=status.HTTP_400_BAD_REQUEST)
        
        if Product.objects.filter(will_buyer=request.data.get('will_buyer', None), seller=Profile.objects.get(user=request.user)):
            return Response({"error": "you are seller!"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        chatroom = serializer.save()
        chatroom.is_active=True
        chatroom.save()
        serializer = self.get_serializer(chatroom)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        chatroom = self.get_object()
        return Response(self.get_serializer(chatroom).data)

    def list(self, request):
        chatrooms = self.get_queryset()
        return Response(self.get_serializer(chatrooms, many=True).data)

    def delete(self, request, pk=None):
        chatroom = self.get_object()
        if ChatRoom.objects.filter(will_buyer=request.data.get('will_buyer', None), product=request.data.get('product', None)).exists():
            chatroom.is_active = False
            chatroom.save()
        else:
            return Response({"error": "you are not buyer in this chat"}, status=status.HTTP_403_FORBIDDEN)
        return Response(self.get_serializer(chatroom).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['PUT', 'POST'])
    def transaction(self, request, pk):
        chatroom = self.get_object()
        user=Profile.objects.get(user=request.user)
        if self.request.method == 'POST':
            return self._transacted(chatroom, user)
        elif self.request.method == 'PUT':
            return self._review

    def _transacted(self, chatroom, user):
        if not chatroom.product.seller==user:
            return Response({"error": "you are not seller"}, status=status.HTTP_403_FORBIDDEN)
        trans = Transaction.objects.create(chatroom=chatroom)
        chatroom.product.status=0
        chatroom.product.buyer=chatroom.will_buyer
        chatroom.product.save()
        return Response(TransactionSerializer(trans).data, status=status.HTTP_201_CREATED)

    def _review(self, chatroom, user):
        if not self.request.get("review", 0):
            return Response({"error": "not all required"}, status=status.HTTP_400_BAD_REQUEST)
        if chatroom.product.seller==user:
            trans = Transaction.objects.get(chatroom=chatroom)
            trans.seller_review=self.request.get("review")
            trans.save()
        else:
            trans = Transaction.objects.get(chatroom=chatroom)
            trans.buyer_review=self.request.get("review")
            trans.save()
        trans = Transaction.objects.get(chatroom=chatroom)
        return Response(TransactionSerializer(trans).data, status=status.HTTP_200_OK)