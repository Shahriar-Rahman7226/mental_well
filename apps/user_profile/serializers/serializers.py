from rest_framework import serializers
from rest_framework.serializers import *

from apps.user_profile.models import *

exclude_list = [
    'is_active',
    'created_at',
    'updated_at'
]


class SpecializationSerializer(ModelSerializer):
    
    class Meta:
        model = SpecializationModel
        exclude = exclude_list


class CounselorProfileCreateSerializer(ModelSerializer):
    
    class Meta:
        model = CounselorProfileModel
        fields = ['user', 'certificate', 'identity_document', 'specializations', 'description', 'license_number', 'website', 'linked_in']


class CounselorProfileUpdateSerializer(ModelField):

    class Meta:
        model = CounselorProfileModel
        fields = ['status']


class CounselorProfileListSerializer(ModelField):

    class Meta:
        model = CounselorProfileModel
        exclude = exclude_list


class ClientProfileCreateSerializer(ModelSerializer):
    
    class Meta:
        model = ClientProfileModel
        fields = ['user', 'description', 'goals', 'emergency_contact']


class ClientProfileUpdateSerializer(ModelField):

    class Meta:
        model = ClientProfileModel
        fields = ['status']


class ClientProfileListSerializer(ModelField):

    class Meta:
        model = ClientProfileModel
        exclude = exclude_list