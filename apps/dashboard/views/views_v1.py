from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import DashboardSerializer, UserStatsSerializer, AppointmentSerializer, ActivityLogSerializer
from apps.user.models import UserModel
from apps.appointments.models import Appointment
from apps.activity.models import ActivityLog

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Example data, replace with actual queries
        user_stats = {
            "total_users": UserModel.objects.count(),
            "active_users": UserModel.objects.filter(is_active=True).count(),
            "new_users": UserModel.objects.filter(date_joined__gte="some_date").count()
        }
        recent_appointments = Appointment.objects.all()[:10]
        recent_activity = ActivityLog.objects.all()[:10]

        data = {
            "user_stats": user_stats,
            "recent_appointments": recent_appointments,
            "recent_activity": recent_activity,
        }

        serializer = DashboardSerializer(data)
        return Response(serializer.data)


class UserStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_stats = {
            "total_users": UserModel.objects.count(),
            "active_users": UserModel.objects.filter(is_active=True).count(),
            "new_users": UserModel.objects.filter(date_joined__gte="some_date").count()
        }
        serializer = UserStatsSerializer(user_stats)
        return Response(serializer.data)


class RecentAppointmentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        recent_appointments = Appointment.objects.all()[:10]
        serializer = AppointmentSerializer(recent_appointments, many=True)
        return Response(serializer.data)


class RecentActivityView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        recent_activity = ActivityLog.objects.all()[:10]
        serializer = ActivityLogSerializer(recent_activity, many=True)
        return Response(serializer.data)
