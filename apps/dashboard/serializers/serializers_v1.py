from rest_framework import serializers
from .models import User, Appointment, ActivityLog

class UserStatsSerializer(serializers.Serializer):
    total_users = serializers.IntegerField()
    active_users = serializers.IntegerField()
    new_users = serializers.IntegerField()

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'client_name', 'counselor_name', 'date', 'time', 'status']

class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = ['id', 'user', 'action', 'timestamp']

class DashboardSerializer(serializers.Serializer):
    user_stats = UserStatsSerializer()
    recent_appointments = AppointmentSerializer(many=True)
    recent_activity = ActivityLogSerializer(many=True)
