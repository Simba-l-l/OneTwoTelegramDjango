from rest_framework import routers
from .api import *
from .views import *
from django.urls import path

router = routers.DefaultRouter()
router.register('api/sneakers', SneakersViewSet, 'Sneakers')
router.register('api/orderlist', OrderListViewSet, 'OrderList')

urlpatterns = [
    path('api/addorder', add_order),
    path('api/proofpayment', proof_of_payment)
] + router.urls

