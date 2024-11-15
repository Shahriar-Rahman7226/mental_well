from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('dashboard/user-stats/', views.UserStatsView.as_view(), name='user-stats'),
    path('dashboard/recent-appointments/', views.RecentAppointmentsView.as_view(), name='recent-appointments'),
    path('dashboard/recent-activity/', views.RecentActivityView.as_view(), name='recent-activity'),
]
