from django.db import models
from abstract.base_model import CustomModel
from apps.user.models import UserModel
from external.choice_tuple import ProfileStatus
# Create your models here.

class SpecializationModel(CustomModel):
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table='specialization'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title if self.title else ''}"
    

class CounselorProfileModel(CustomModel):
    user = models.ForeignKey(UserModel, related_name='counselor_profile', on_delete=models.CASCADE, blank=True, null=True)
    certificate = models.FileField(blank=True, null=True)
    identity_document = models.FileField(blank=True, null=True)
    specializations = models.ManyToManyField(SpecializationModel, related_name='counselor_specialization')
    description = models.TextField(blank=True, null=True)
    license_number = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    linked_in = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True, choices=ProfileStatus, default=ProfileStatus[0][0])

    

    class Meta:
        db_table='counselor_profile'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.first_name if self.user else ''} {self.user.last_name if self.user else ''} -- {self.status if self.status else ''}" 
    


class ClientProfileModel(CustomModel):
    user = models.ForeignKey(UserModel, related_name='client_profile', on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    goals = models.TextField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=20, blank=True, null=True, unique=True)
    status = models.CharField(max_length=100, blank=True, null=True, choices=ProfileStatus, default=ProfileStatus[0][0])

    

    class Meta:
        db_table='client_profile'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.first_name if self.user else ''} {self.user.last_name if self.user else ''} -- {self.status if self.status else ''}" 