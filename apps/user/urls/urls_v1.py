from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user.views.views_v1 import *
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register('user-registration', UserResgistrationViewSet, basename='user_registration')

urlpatterns = [
                  path(r'', include(router.urls)),
                  path('create-admin/', UserResgistrationViewSet.as_view({'post': 'create_admin'})),
                  path('create-manager/', UserResgistrationViewSet.as_view({'post': 'create_manager'})),
                  path('create-customer/', UserResgistrationViewSet.as_view({'post': 'create_customer'})),
              ] 
