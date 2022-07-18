from .models import *
from rest_framework import viewsets, permissions
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json


class SneakersViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = SneakersSerializer

    def get_queryset(self):

        # filter_params = json.loads(self.request.body.decode("utf-8"))

        print(self.request.body)

        queryset = Sneaker.objects.all()
        # sneaker_id = filter_params['id']
        # brand = filter_params['brand']
        # gender = filter_params['gender']
        # max_price = filter_params['max_price']
        # min_price = filter_params['min_price']
        # sizes = filter_params['sizes']
        #
        # if gender == 'M':
        #     queryset = queryset.exclude(gender='W')
        # elif gender == 'W':
        #     queryset = queryset.exclude(gender='M')
        #
        # if sneaker_id is not None:
        #     queryset = queryset.filter(id=sneaker_id)
        #
        # if brand is not None:
        #     queryset = queryset.filter(brand=brand)
        #
        # if max_price is not None:
        #     queryset = queryset.filter(price__lte=max_price)
        #
        # if min_price is not None:
        #     queryset = queryset.filter(price__gte=min_price)
        #
        # if sizes is not None:
        #     queryset = queryset.filter()

        return queryset


class OrderListViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post']
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = OrderListSerializer
    queryset = OrderList.objects.all()


@api_view(['POST'])
def add_order(request):
    order_info = json.loads(request.body.decode("utf-8"))
    order = OrderList(
        customer=order_info['order_list']['customer'],
        shipping_address=order_info['order_list']['shipping_address'],
        phone_number=order_info['order_list']['phone_number'],
        is_paid=True
    )
    for item in order_info['order_items']:
        if not Sneaker.objects.filter(id=item['sneaker_id']).exists():
            return Response({'e': 'No such sneaker_id'}, status.HTTP_400_BAD_REQUEST)
    order.save()
    for item in order_info['order_items']:
        sneaker = Sneaker.objects.get(id=item['sneaker_id'])
        cur_item = OrderItem(
            order_id=order,
            sneaker_id=sneaker,
            sneaker_size=item['sneaker_size'],
            quantity=item['quantity']
        )
        cur_item.save()
    return Response({'order_id': order.order_id}, status.HTTP_200_OK)


@api_view(['GET'])
def check_server(request):
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def get_sneakers(request):
    print(request.body)
    for i in Sneaker.objects.all():
        print(i.brand)
    return Response(status=status.HTTP_200_OK)
