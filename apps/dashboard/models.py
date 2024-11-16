from django.db import models
from apps.user.models import UserModel
from abstract.base_model import CustomModel
from apps.user_profile.models import *
from external.choice_tuple import Days, AdminStatus, ClientOverview, PackageType, PaymentMethodType, ReviewStatus


# ----- GENERAL MODELS -----
class BannerModel(CustomModel):
    title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='banner/', blank=True, null=True)

    class Meta:
        db_table='banner_model'
        ordering=['-created_at']


class MotivationModel(CustomModel):
    quote_text = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table='motivation_model'
        ordering=['-created_at']


class Resources(CustomModel):
    title = models.CharField(max_length=100, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    resource_file = models.FileField(blank=True, null=True)
    resource_link = models.URLField(blank=True, null=True)

    class Meta:
        db_table='resources'
        ordering=['-created_at']


class LegalDocument(CustomModel):
    details = models.TextField(blank=True, null=True)
    version = models.CharField(max_length=100, blank=True, null=True)
    licence_document = models.FileField(blank=True, null=True)

    class Meta:
        db_table='legal_document'
        ordering=['-created_at']


class PrivacyPolicy(CustomModel):
    details = models.TextField(blank=True, null=True)

    class Meta:
        db_table='privacy_policy'
        ordering=['-created_at']


class AboutUs(CustomModel):
    introduction = models.TextField(blank=True, null=True)
    mission_statement = models.TextField(blank=True, null=True)
    vision_statement = models.TextField(blank=True, null=True)
    history = models.TextField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    contact_number = models.CharField(max_length=100, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    class Meta:
        db_table='about_us'
        ordering=['-created_at']


class FooterModel(CustomModel):
    image = models.ImageField(upload_to='footer/', blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    contact_number = models.CharField(max_length=100, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    emergency_support = models.TextField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    class Meta:
        db_table='footer_models'
        ordering=['-created_at']


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


class ClientProgress(CustomModel):
    counselor = models.ForeignKey(CounselorProfileModel, related_name='client_progress_counselor', on_delete=models.CASCADE, blank=True, null=True)
    client = models.ForeignKey(ClientProfileModel, related_name='client_progress_client', on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True, choices=ClientOverview, default=ClientOverview[0][0])
    session_count = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        db_table='client_progress'
        ordering=['-created_at']


class ClientProgressDetails(CustomModel):
    overview = models.ForeignKey(ClientProfileModel, related_name='progress_details', on_delete=models.CASCADE, blank=True, null=True)
    appointment = models.ForeignKey(AppointmentRequest, related_name='progress_appointment', on_delete=models.CASCADE, blank=True, null=True)
    details = models.TextField(blank=True, null=True)

    class Meta:
        db_table='client_progress_details'
        ordering=['-created_at']


class Achievements(CustomModel):
    counselor = models.ForeignKey(CounselorProfileModel, related_name='counselor_achievements', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    awarded_by = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)

    class Meta:
        db_table='achievements'
        ordering=['-created_at']


class Article(CustomModel):
    thumbnail = models.ImageField(upload_to='article/', blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True) 
    author = models.ForeignKey(CounselorProfileModel, related_name='author_article', on_delete=models.CASCADE, blank=True, null=True)
    author_name = models.CharField(max_length=100, blank=True, null=True)  
    article_file = models.FileField(blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)  
    status = models.CharField(max_length=100, blank=True, null=True, choices=ReviewStatus, default=ReviewStatus[0][0])
    is_published = models.BooleanField(blank=True, null=True) 

    def __str__(self):
        return f"{self.title if self.title else ''} - {self.author_name if self.author_name else ''}"

    class Meta:
        db_table='article'
        ordering = ['-created_at'] 


class VideoJournal(CustomModel):
    thumbnail = models.ImageField(upload_to='video_journal/', blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True) 
    author = models.ForeignKey(CounselorProfileModel, related_name='author_video_journal', on_delete=models.CASCADE, blank=True, null=True)
    author_name = models.CharField(max_length=100, blank=True, null=True)  
    journal_link = models.URLField(blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True, choices=ReviewStatus, default=ReviewStatus[0][0])
    is_published = models.BooleanField(blank=True, null=True) 
  

    def __str__(self):
        return f"{self.title if self.title else ''} - {self.author_name if self.author_name else ''}"

    class Meta:
        db_table='video_journal'
        ordering = ['-created_at'] 


# ----- CLIENT MODELS -----
class FAQModel(CustomModel):
    client = models.ForeignKey(UserModel, related_name='faq_client', on_delete=models.CASCADE, blank=True, null=True)
    question = models.TextField(blank=True, null=True)
    asnwer = models.TextField(blank=True, null=True)
    is_published = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table='faq_model'
        ordering=['-created_at']


# Payment Form
class Payment(CustomModel):
    counselor = models.ForeignKey(
        CounselorProfileModel, 
        related_name='counselor_payment', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    client = models.ForeignKey(
        ClientProfileModel, 
        related_name='client_payment', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    appointment = models.ForeignKey(
        AppointmentRequest, 
        related_name='appointment_schedule', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    due_amount = models.FloatField(
        blank=True, 
        null=True, 
        default=500  # Defaulting to 500 Taka per session
    )
    paid_amount = models.FloatField(
        blank=True, 
        null=True
    )
    payment_date = models.DateField(
        blank=True, 
        null=True
    )
    transaction_id = models.CharField(
        max_length=255, 
        blank=True, 
        null=True
    )
    payment_method = models.CharField(
        max_length=100, 
        choices=PaymentMethodType, 
        default=PaymentMethodType[0][0], 
        blank=True, 
        null=True
    )

    class Meta:
        db_table = 'payment'

    def __str__(self):
        first_name = self.client.user.first_name if self.client and self.client.user else ''
        last_name = self.client.user.last_name if self.client and self.client.user else ''
        transaction_id = self.transaction_id if self.transaction_id else ''
        return f"{first_name} {last_name} - {transaction_id}"


# #Session Price and Booking
# class SessionPackage(CustomModel):
#     package = models.CharField(max_length=100, choices=PackageType, unique=True, blank=True, null=True)
#     price = models.FloatField(max_digits=10, decimal_places=2, blank=True, null=True)
#     sessions_count = models.PositiveIntegerField(default=0, blank=True, null=True)

#     class Meta:
#         db_table = 'session_package'


class Review(CustomModel):
    counselor = models.ForeignKey(CounselorProfileModel, related_name='counselor_review', on_delete=models.CASCADE, blank=True, null=True)
    client = models.ForeignKey(ClientProfileModel, related_name='client_review', on_delete=models.CASCADE, blank=True, null=True)
    rating = models.PositiveIntegerField(blank=True, null=True) 
    review_text = models.TextField(blank=True, null=True)
    client_name = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True, choices=ReviewStatus, default=ReviewStatus[0][0])
    is_published = models.BooleanField(blank=True, null=True) 
    appointment_count = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.client_name if self.client_name else ''} - {self.rating if self.rating else ''}"

    class Meta:
        db_table = 'review'
        ordering = ['-created_at'] 