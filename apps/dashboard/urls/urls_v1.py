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
router.register('appointment-request', AppointmentRequestViewSet, basename='appointment_request')
router.register('client-progress', ClientProgressViewSet, basename='client_progress')
router.register('client-progress-details', ClientProgressDetailsViewSet, basename='client_progress_details')
router.register('achievements', AchievementsViewSet, basename='achievements')
router.register('article', ArticleViewSet, basename='article')
router.register('video-journal', VideoJournalViewSet, basename='video_journal')
router.register('faq', FAQViewSet, basename='faq')
router.register('review', ReviewViewSet, basename='review')
router.register('payment', PaymentViewSet, basename='payment')

urlpatterns = [
    path(r'', include(router.urls)),
     path('get-schedule/', CounselorScheduleViewSet.as_view({'get': 'get_schedule'})),
     path('get-request/', AppointmentRequestViewSet.as_view({'get': 'get_request'})),
     path('get-counselor-payment-history/', PaymentViewSet.as_view({'get': 'get_counselor_payment_history'})),
     path('get-client-payment-history/', PaymentViewSet.as_view({'get': 'get_client_payment_history'})),
]