# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.dashboard.views.views_v1 import *
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register('banner', BannerViewSet, basename='banner')
router.register('motivation', MotivationViewSet, basename='motivation')
router.register('resources', ResourcesViewSet, basename='resources')
router.register('legal-document', LegalDocumentViewSet, basename='legal_document')
router.register('privacy-policy', PrivacyPolicyViewSet, basename='privacy_policy')
router.register('about-us', AboutUsViewSet, basename='about_us')
router.register('footer', FooterViewSet, basename='footer')
router.register('counselor-schedule', CounselorScheduleViewSet, basename='counselor_schedule')

urlpatterns = [
    path(r'', include(router.urls)),
     path('get_schedule/', CounselorScheduleViewSet.as_view({'get': 'get_schedule'})),
    # path('counselor-schedules/', views.CounselorScheduleListCreateView.as_view(), name='counselor_schedule_list_create'),
    # path('counselor-schedules/<int:pk>/', views.CounselorScheduleDetailView.as_view(), name='counselor_schedule_detail'),
    # path('appointments/', views.AppointmentRequestListCreateView.as_view(), name='appointment_list_create'),
    # path('appointments/<int:pk>/', views.AppointmentRequestDetailView.as_view(), name='appointment_detail'),
    # path('session-packages/', views.SessionPackageListView.as_view(), name='session_package_list'),
    # path('make-payment/', views.PaymentCreateView.as_view(), name='make_payment'),
]