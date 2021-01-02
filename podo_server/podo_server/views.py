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


class ChatRoomViewSet(viewsets.GenericViewSet):
    queryset = ChatRoom.object.all()
    serializer_class = ChatRoomSerializer
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        return super(ProductViewSet, self).get_permissions()

    def get_serializer_class(self):
        return self.serializer_class

    def create(self, request):
        user = request.user

        if ChatRoom.objects.filter(buy_id=user, product_id=request.data.get('product_id')).exists():  # buyer_id=user?
            return Response({"error": "You have already chatroom"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        chatroom = serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        chatroom = self.get_object()
        user = request.user
        if ChatRoom.objects.filter(buy_ie=user, product_id=request.data.get('product_id')).exists():
            chatroom.is_active = False
        return Response(self.get_serializer(chatroom).data)


    @action(detail=True, methods=['POST', 'GET'])
    def Message(self, request, pk):
        chatroom = self.get_object()

        if self.request.method == 'POST':
            return self._send_message
        else:
            return self._petch_message

    def _send_message(self, chatroom):
        Message.objets.create(chatroom=chatroom, body=self.request.data.get('body'), written_by=self.request.user)
        return Response(status=status.HTTP_201_CREATED)

    def _petch_message(self, chatroom):
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
<<<<<<< HEAD
=======


    @action(detail=True, methods=['PUT', 'POST', 'DELETE'])
    def appointment(self, request, pk):
        chatroom = self.get_object()

        if self.request.method == 'POST':
            return self._suggest_appo
        elif self.request.method == 'PUT':
            return self._confirm_appo
        else:
            return self._deny_appo

    def _suggest_appo(self, chatroom):
        serializer = AppointmentSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        price = serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _confirm_appo(self, chatroom):
        appointment = Appointment.objects.get(chatroom_id=chatroom)
        appointment.confirm = True
        return Response(AppointmentSerializer(appointment).data, status=status.HTTP_200_OK)

    def _deny_appo(self, chatroom):
        appointment = Appointment.objects.get(chatroom_id=chatroom).delete()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['PUT', 'POST', 'DELETE'])
    def suggestprice(self, request, pk):
        chatroom = self.get_object()

        if self.request.method == 'POST':
            return self._suggest_price
        elif self.request.method == 'PUT':
            return self._confirm_price
        else:
            return self._deny_price

    def _suggest_price(self, chatroom):
        serializer = SuggestPriceSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        price = serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _confirm_price(self, chatroom):
        suggestion = SuggestPrice.objects.get(chatroom_id=chatroom)
        suggestion.confirm = True
        return Response(SuggestPriceSerializer(suggestion).data, status=status.HTTP_200_OK)

    def _deny_price(self, chatroom):
        suggestion = SuggestPrice.objects.get(chatroom_id=chatroom).delete()
        return Response(status=status.HTTP_200_OK)
>>>>>>> 1db2be9... suggestprice api
