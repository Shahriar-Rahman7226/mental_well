# serializers.py
from rest_framework import serializers
from .models import CounselorSchedule, AppointmentRequest
from .models import SessionPackage, Payment

class CounselorScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CounselorSchedule
        fields = '__all__'

class AppointmentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentRequest
        fields = '__all__'


class SessionPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionPackage
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
