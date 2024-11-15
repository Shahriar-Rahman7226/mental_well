from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE) 
    counselor_name = models.CharField(max_length=200)  
    rating = models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]) 
    review_text = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Review by {self.client.username} for {self.counselor_name}"

    class Meta:
        ordering = ['-created_at'] 

        


       class Article(models.Model):
    title = models.CharField(max_length=200) 
    author = models.ForeignKey(User, on_delete=models.CASCADE)  
    content = models.TextField()  # Full content of the article
    published_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_at'] 




        class Vlog(models.Model):
    title = models.CharField(max_length=200)  
    video_url = models.URLField()  
    description = models.TextField()  
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)  
    posted_at = models.DateTimeField(auto_now_add=True) 
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-posted_at'] 
from abstract.base_model import CustomModel
from apps.user_profile.models import *
from external.choice_tuple import Days, AdminStatus, ClientOverview, PackageType, PaymentMethodType

# ----- COUNSELOR MODELS -----
# Available time slots or schedules for each counselor
class CounselorSchedule(CustomModel):
    counselor = models.ForeignKey(CounselorProfileModel, related_name='counselor_schedule', on_delete=models.CASCADE, blank=True, null=True)
    day = models.CharField(max_length=100, blank=True, null=True, choices=Days)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    is_available = models.BooleanField(blank=True, null=True, default=True)
    is_booked = models.BooleanField(blank=True, null=True, default=False)
    status = models.CharField(max_length=100, blank=True, null=True, choices=AdminStatus, default=AdminStatus[0][0])

    class Meta:
        db_table='counselor_schedule'
        ordering=['-created_at']

    def __str__(self):
        return f"{self.client.user.first_name if self.client.user else ''} {self.client.user.last_name if self.client.user else ''} - {self.day if self.day else ''}"


# When clients book appointments with counselors
class AppointmentRequest(CustomModel):
    counselor = models.ForeignKey(CounselorProfileModel, related_name='counselor_request', on_delete=models.CASCADE, blank=True, null=True)
    client = models.ForeignKey(ClientProfileModel, related_name='client_request', on_delete=models.CASCADE, blank=True, null=True)
    schedule = models.ForeignKey(CounselorSchedule, related_name='appointment_schedule', on_delete=models.CASCADE, blank=True, null=True)
    booking_date = models.DateTimeField(blank=True, null=True)
    status=models.CharField(max_length=100, blank=True, null=True, choices=AdminStatus, default=AdminStatus[0][0])
    is_paid = models.BooleanField(blank=True, null=True, default=False)

    class Meta:
        db_table='appointment_request'
        ordering=['-created_at']
    
    def __str__(self):
        return f"{self.client.user.first_name if self.client.user else ''} {self.client.user.last_name if self.client.user else ''} - {self.status if self.status else ''}"


#Payment Type
class Payment(CustomModel):
    counselor = models.ForeignKey(CounselorProfileModel, related_name='counselor_payment', on_delete=models.CASCADE, blank=True, null=True)
    client = models.ForeignKey(ClientProfileModel, related_name='client_payment', on_delete=models.CASCADE, blank=True, null=True)
    # package = models.ForeignKey(SessionPackage, on_delete=models.CASCADE)
    appointment = models.ForeignKey(AppointmentRequest, related_name='appointment_schedule', on_delete=models.CASCADE, blank=True, null=True)
    due_amount = models.FloatField(blank=True, null=True)
    paid_amount = models.FloatField(blank=True, null=True)
    payment_date = models.DateField(blank=True, null=True)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    payment_method = models.CharField(max_length=100, choices=PaymentMethodType, default=PaymentMethodType[0][0], blank=True, null=True)

    class Meta:
        db_table = 'payment'

    def __str__(self):
        return f"{self.client.user.first_name if self.client.user else ''} {self.client.user.last_name if self.client.user else ''} - {self.transaction_id if self.transaction_id else ''}"


# #Session Price and Booking
# class SessionPackage(CustomModel):
#     package = models.CharField(max_length=100, choices=PackageType, unique=True, blank=True, null=True)
#     price = models.FloatField(max_digits=10, decimal_places=2, blank=True, null=True)
#     sessions_count = models.PositiveIntegerField(default=0, blank=True, null=True)

#     class Meta:
#         db_table = 'session_package'


