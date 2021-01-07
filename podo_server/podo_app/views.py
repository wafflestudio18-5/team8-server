from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from podo_app.models import *
from podo_app.serializers import *

class ProductViewSet(viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ('create'):
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
            products = products.filter(product__category=category)
        if city:
            products = products.filter(product__city=city)
        return Response(self.get_serializer(products, many=True).data)


    @action(detail=True, methods=['PUT', 'POST', 'DELETE'])
    def suggestprice(self, request, pk):
        product = self.get_object()

        if self.request.method == 'POST':
            return self._suggest_price
        elif self.request.method == 'PUT':
            return self._confirm_price
        else:
            return self._deny_price

    def _suggest_price(self, product):
        if not product.allow_suggest:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = SuggestPriceSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        price = serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _confirm_price(self, product):
        suggestion = product.chatrooms.suggest_price
        suggestion.confirm = True
        return Response(SuggestPriceSerializer(suggestion).data, status=status.HTTP_200_OK)

    def _deny_price(self, product):
        suggestion = product.chatrooms.suggest_price.delete()
        return Response(status=status.HTTP_200_OK)

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
        return super(ProductViewSet, self).get_permissions()

    def get_serializer_class(self):
        return self.serializer_class

    def create(self, request):
        if ChatRoom.objects.filter(will_buyer=request.data.get('will_buyer', None), product=request.data.get('product', None)).exists(): 
            return Response({"error": "You have already chatroom"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        chatroom = serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        chatroom = self.get_object()
        if ChatRoom.objects.filter(will_buyer=request.data.get('will_buyer', None), product=request.data.get('product', None)).exists():
            chatroom.is_active = False
        return Response(self.get_serializer(chatroom).data)

    @action(detail=True, methods=['PUT', 'POST'])
    def transaction(self, request, pk):
        chatroom = self.get_object()

        if self.request.method == 'POST':
            return self._transacted
        elif self.request.method == 'PUT':
            return self._review

    def _transacted(self, chatroom):
        #check seller
        serializer = TransactionSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        price = serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _review(self, chatroom):
        return