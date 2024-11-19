from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.payment.views.views_v1 import PaymentViewSet

router = DefaultRouter()
router.register('payment', PaymentViewSet, basename='payment')

urlpatterns = [
    path(r'', include(router.urls)),
     path('get-counselor-payment-history/', PaymentViewSet.as_view({'get': 'get_counselor_payment_history'})),
     path('get-client-payment-history/', PaymentViewSet.as_view({'get': 'get_client_payment_history'})),
]