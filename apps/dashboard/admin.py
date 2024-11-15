from django.contrib import admin
from apps.user.models import UserModel
from apps.appointments.models import Appointment
from apps.activity.models import ActivityLog

# Customizing the admin view for UserModel
@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'email', 'is_active', 'date_joined')
    search_fields = ('phone_number', 'email')
    list_filter = ('is_active', 'date_joined')
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined', 'last_login')
    
    # If UserModel has sensitive data, limit fields shown in the admin
    fields = ('phone_number', 'email', 'is_active', 'date_joined', 'last_login')


# Customizing the admin view for Appointment
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'counselor', 'scheduled_date', 'status')
    search_fields = ('user__phone_number', 'counselor__name')
    list_filter = ('status', 'scheduled_date')
    ordering = ('-scheduled_date',)
    
    # Define fields to include in the detailed appointment view
    fields = ('user', 'counselor', 'scheduled_date', 'status', 'notes')


# Customizing the admin view for ActivityLog
@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'action', 'timestamp')
    search_fields = ('user__phone_number', 'action')
    list_filter = ('action', 'timestamp')
    ordering = ('-timestamp',)

    # Define which fields are shown in the detailed activity log view
    fields = ('user', 'action', 'timestamp')
