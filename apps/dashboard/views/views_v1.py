# views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CounselorSchedule, AppointmentRequest
from .serializers import CounselorScheduleSerializer, AppointmentRequestSerializer
from .models import SessionPackage, Payment
from .serializers import SessionPackageSerializer, PaymentSerializer
import requests
from .serializers import PaymentSerializer
from django.conf import settings

# Counselor Schedule Views
class CounselorScheduleListCreateView(generics.ListCreateAPIView):
    queryset = CounselorSchedule.objects.all()
    serializer_class = CounselorScheduleSerializer
    permission_classes = [IsAuthenticated]

class CounselorScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CounselorSchedule.objects.all()
    serializer_class = CounselorScheduleSerializer
    permission_classes = [IsAuthenticated]

# Appointment Request Views
class AppointmentRequestListCreateView(generics.ListCreateAPIView):
    queryset = AppointmentRequest.objects.all()
    serializer_class = AppointmentRequestSerializer
    permission_classes = [IsAuthenticated]

class AppointmentRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AppointmentRequest.objects.all()
    serializer_class = AppointmentRequestSerializer
    permission_classes = [IsAuthenticated]


# List available session packages
class SessionPackageListView(generics.ListAPIView):
    queryset = SessionPackage.objects.all()
    serializer_class = SessionPackageSerializer
    permission_classes = [IsAuthenticated]

# Payment view (Example for demonstration, real implementation would include transaction logic)
class PaymentCreateView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# views.py

class PaymentCreateView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        payment_method = self.request.data.get("payment_method")
        package_id = self.request.data.get("package_id")
        amount = self.request.data.get("amount")
        
        if payment_method == "BKASH":
            # Example of bKash API Call
            bkash_response = self.initiate_bkash_payment(amount)
            if bkash_response.get("status") == "Success":
                transaction_id = bkash_response.get("transaction_id")
                serializer.save(user=self.request.user, payment_method="BKASH", transaction_id=transaction_id, is_successful=True)
            else:
                serializer.save(user=self.request.user, payment_method="BKASH", is_successful=False)

        elif payment_method == "NAGAD":
            # Example of Nagad API Call
            nagad_response = self.initiate_nagad_payment(amount)
            if nagad_response.get("status") == "Success":
                transaction_id = nagad_response.get("transaction_id")
                serializer.save(user=self.request.user, payment_method="NAGAD", transaction_id=transaction_id, is_successful=True)
            else:
                serializer.save(user=self.request.user, payment_method="NAGAD", is_successful=False)

    def initiate_bkash_payment(self, amount):
        # Placeholder code to initiate a bKash payment
        url = "<your_bkash_endpoint>"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer <access_token>"
        }
        data = {
            "amount": amount,
            # add other required parameters for bKash
        }
        response = requests.post(url, json=data, headers=headers)
        return response.json()

    def initiate_nagad_payment(self, amount):
        # Placeholder code to initiate a Nagad payment
        url = "<your_nagad_endpoint>"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer <access_token>"
        }
        data = {
            "amount": amount,
            # add other required parameters for Nagad
        }
        response = requests.post(url, json=data, headers=headers)
        return response.json()
