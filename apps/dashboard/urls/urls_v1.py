# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('counselor-schedules/', views.CounselorScheduleListCreateView.as_view(), name='counselor_schedule_list_create'),
    path('counselor-schedules/<int:pk>/', views.CounselorScheduleDetailView.as_view(), name='counselor_schedule_detail'),
    path('appointments/', views.AppointmentRequestListCreateView.as_view(), name='appointment_list_create'),
    path('appointments/<int:pk>/', views.AppointmentRequestDetailView.as_view(), name='appointment_detail'),
]


urlpatterns = [
    path('session-packages/', views.SessionPackageListView.as_view(), name='session_package_list'),
    path('make-payment/', views.PaymentCreateView.as_view(), name='make_payment'),
]
