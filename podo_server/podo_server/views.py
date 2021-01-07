from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..podo_app.models import Product, LikeProduct, ChatRoom, Message
from ..podo_server.serializers import *

def ping(request):
    return HttpResponse('pong-dong')


class ProductViewSet(viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated, )

    def get_permissions(self):
        return super(ProductViewSet, self).get_permissions()

    def get_serializer_class(self):
        return self.serializer_class

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        product = self.get_object()
        return Response(self.get_serializer(product).data)

    def list(self, request):
        name = request.query_params.get('name')
        order = request.query_params.get('order')
        max_price = request.query_params.get('max_price')
        category = request.query_params.get('category')

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
            products = products.filter(category__icontains=category)
        return Response(self.get_serializer(products, many=True).data)
