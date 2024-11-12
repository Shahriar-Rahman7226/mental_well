from django.db import models
from abstract.base_model import CustomModel
from apps.user_profile.models import *
from external.choice_tuple import Days, AppointmentStatus


#Available time slots or schedules for each counselor
class CounselorSchedule(CustomModel):
    counselor = models.ForeignKey(CounselorProfileModel, related_name='counselor_schedule', on_delete=models.CASCADE, blank=True, null=True)
    day = models.CharField(max_length=100, blank=True, null=True, choices=Days)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    is_available = models.BooleanField(default=True, blank=True, null=True)
    booked = models.BooleanField(default=False, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table='counselor_schedule'
        ordering=['-created_at']

    def __str__(self):
        return f"{self.counselor.user.first_name if self.counselor.user else ''} {self.counselor.user.last_name if self.counselor.user else ''} - {self.day if self.day else ''}"
    
#When clients book appointments with counselors
class AppointmentRequest(CustomModel):
    counselor = models.ForeignKey(CounselorProfileModel, related_name='counselor_schedule', on_delete=models.CASCADE, blank=True, null=True)
    client_email = models.EmailField(blank=True, null=True)
    client_number = models.CharField(max_length=100, blank=True, null=True)
    schedule = models.ForeignKey(CounselorSchedule, related_name='appointment_schedule', on_delete=models.CASCADE, blank=True, null=True)
    booking_date = models.DateTimeField(blank=True, null=True)
    status=models.CharField(max_length=100, blank=True, null=True, choices=AppointmentStatus, default='PENDING')

    class Meta:
        db_table='appointment_request'
        ordering=['-created_at']
    
    def __str__(self):
        return f"{self.counselor.user.first_name if self.counselor.user else ''} {self.counselor.user.last_name if self.counselor.user else ''} - {self.client_email if self.client_email else ''}" (Create views for this)

#Session Price and Booking
class SessionPackage(models.Model):
    PACKAGE_CHOICES = [
        ('SINGLE', 'Single Session'),
        ('FIVE', '5-Session Package'),
    ]
    
    name = models.CharField(max_length=50, choices=PACKAGE_CHOICES, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sessions_included = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'session_package'

    def __str__(self):
        return f"{self.get_name_display()} - ${self.price}"

    @staticmethod
    def create_default_packages():
        single_session, _ = SessionPackage.objects.get_or_create(
            name='SINGLE',
            defaults={'price': 20.00, 'sessions_included': 1}
        )
        package_session, _ = SessionPackage.objects.get_or_create(
            name='FIVE',
            defaults={'price': 80.00, 'sessions_included': 5}
        )


#Payment Type
class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('BKASH', 'bKash'),
        ('NAGAD', 'Nagad'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    package = models.ForeignKey(SessionPackage, on_delete=models.CASCADE)
    counselor = models.ForeignKey(CounselorProfileModel, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=50, default="Pending")

    class Meta:
        db_table = 'payment'

    def __str__(self):
        return f"{self.user.username} - {self.package.name} - {'Success' if self.is_successful else 'Failed'}"

