from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from external.pagination import CustomPagination
from external.swagger_query_params import set_query_params
from apps.dashboard.serializers.serializers_v1 import *
from ..models import *
from external.send_message import send_email, send_sms
from rest_framework import status
from external.permission_decorator import allowed_users
import time


@extend_schema(tags=['Banner'])
class BannerViewSet(ModelViewSet):
    model_class = BannerModel
    serializer_class = BannerSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Banner",
                value={
                    "title": "string",
                    "image": "string",
                },
                request_only=True,
            )
        ],
    )
    @allowed_users(allowed_roles=['ADMIN'])
    def update(self, request, *args, **kwargs):
      
        instance = self.model_class.objects.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'Banner does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Banner updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=request.user.id).first()
        if not obj:
            return Response({'message': 'Banner does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.serializer_class
        serializer = serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@extend_schema(tags=['Motivation'])
class MotivationViewSet(ModelViewSet):
    model_class = MotivationModel
    serializer_class = MotivationSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    @extend_schema(
        examples=[
            OpenApiExample(
                "Create Motivational Quote",
                value={
                    "quote_text": "string",
                    "author": "string",
                },
                request_only=True,
            )
        ]
    )
    @transaction.atomic()
    @allowed_users(allowed_roles=['ADMIN'])
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Motivational quote created succesfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Motivational Quote",
                value={
                    "quote_text": "string",
                    "author": "string",
                },
                request_only=True,
            )
        ],
    )
    @allowed_users(allowed_roles=['ADMIN'])
    def update(self, request, *args, **kwargs):
      
        instance = self.queryset.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'Motivational Quote does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Motivational Quote updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @allowed_users(allowed_roles=['ADMIN'])
    def list(self, request, *args, **kwargs):
        queryset = self.queryset
    
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=request.user.id).first()
        if not obj:
            return Response({'message': 'Motivational Quote does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@extend_schema(tags=['Resources'])
class ResourcesViewSet(ModelViewSet):
    model_class = Resources
    serializer_class = ResourcesSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    @extend_schema(
        examples=[
            OpenApiExample(
                "Create Resource",
                value={
                    "title": "string",
                    "details": "string",
                    "resource_file": "string",
                    "resource_link": "string",
                },
                request_only=True,
            )
        ]
    )
    @transaction.atomic()
    @allowed_users(allowed_roles=['ADMIN'])
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Resource created succesfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Resource",
                value={
                    "title": "string",
                    "details": "string",
                    "resource_file": "string",
                    "resource_link": "string",
                },
                request_only=True,
            )
        ],
    )
    @allowed_users(allowed_roles=['ADMIN'])
    def update(self, request, *args, **kwargs):
      
        instance = self.queryset.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'Resource does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Resource updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def list(self, request, *args, **kwargs):
        queryset = self.queryset
    
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=request.user.id).first()
        if not obj:
            return Response({'message': 'Resource does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@extend_schema(tags=['Legal Document'])
class LegalDocumentViewSet(ModelViewSet):
    model_class = LegalDocument
    serializer_class = LegalDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Legal Document",
                value={
                    "details": "string",
                    "version": "string",
                    "licence_document": "string",
                },
                request_only=True,
            )
        ],
    )
    @allowed_users(allowed_roles=['ADMIN'])
    def update(self, request, *args, **kwargs):
      
        instance = self.model_class.objects.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'Legal Document does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Legal Document updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=request.user.id).first()
        if not obj:
            return Response({'message': 'Legal Document does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.serializer_class
        serializer = serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@extend_schema(tags=['Privacy Policy'])
class PrivacyPolicyViewSet(ModelViewSet):
    model_class = PrivacyPolicy
    serializer_class = PrivacyPolicySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Privacy Policy",
                value={
                    "details": "string",
                },
                request_only=True,
            )
        ],
    )
    @allowed_users(allowed_roles=['ADMIN'])
    def update(self, request, *args, **kwargs):
      
        instance = self.model_class.objects.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'Privacy Policy does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Privacy Policy updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=request.user.id).first()
        if not obj:
            return Response({'message': 'Privacy Policy does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.serializer_class
        serializer = serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@extend_schema(tags=['About Us'])
class AboutUsViewSet(ModelViewSet):
    model_class = AboutUs
    serializer_class = AboutUsSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    @extend_schema(
        examples=[
            OpenApiExample(
               "Update About Us",
                value={
                    "introduction": "string",
                    "mission": "string",
                    "vission": "string",
                    "details": "string",
                    "contact_email": "string",
                    "contact_number": "string",
                    "address": "string",
                    "facebook": "string",
                    "instagram": "string",
                    "youtube": "string",
                    "linkedin": "string",
                },
                request_only=True,
            )
        ],
    )
    @allowed_users(allowed_roles=['ADMIN'])
    def update(self, request, *args, **kwargs):
      
        instance = self.model_class.objects.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'About Us does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'About Us updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=request.user.id).first()
        if not obj:
            return Response({'message': 'About Us does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.serializer_class
        serializer = serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@extend_schema(tags=['Footer'])
class FooterViewSet(ModelViewSet):
    model_class = FooterModel
    serializer_class = FooterSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Footer",
                value={
                    "image": "string",
                    "details": "string",
                    "contact_email": "string",
                    "contact_number": "string",
                    "address": "string",
                    "emergency_support": "string",
                    "facebook": "string",
                    "instagram": "string",
                    "youtube": "string",
                    "linkedin": "string",
                },
                request_only=True,
            )
        ],
    )
    @allowed_users(allowed_roles=['ADMIN'])
    def update(self, request, *args, **kwargs):
      
        instance = self.model_class.objects.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'Footer does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Footer updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=request.user.id).first()
        if not obj:
            return Response({'message': 'Footer does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.serializer_class
        serializer = serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@extend_schema(tags=['Counselor Schedule'])
class CounselorScheduleViewSet(ModelViewSet):
    model_class = CounselorSchedule
    serializer_class = CounselorScheduleSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    @extend_schema(
        examples=[
            OpenApiExample(
                "Create Counselor Schedule",
                value={
                    "counselor": "string",
                    "day": "string",
                    "start_time": "string",
                    "end_time": "string",
                    "is_available": "string",
                    "is_booked": "string",
                },
                request_only=True,
            )
        ]
    )
    @transaction.atomic()
    @allowed_users(allowed_roles=['COUNSELOR'])
    def create(self, request, *args, **kwargs):
        data = request.data
        instance = CounselorProfileModel.objects.filter(user__id=data['counselor'], user__user_role='COUNSELOR').first()
        if not instance:
            return Response({'message': 'Invalid Counselor'}, status=status.HTTP_400_BAD_REQUEST)

        if data['start_time'] > data['end_time']:
            return Response({'message': 'Start time cannot be greater than end time'}, status=status.HTTP_400_BAD_REQUEST)
       
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Counselor schedule created succesfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Counselor Schedule",
                value={
                    "counselor": "string",
                    "day": "string",
                    "start_time": "string",
                    "end_time": "string",
                    "is_available": "string",
                    "is_booked": "string",
                },
                request_only=True,
            )
        ],
    )
    @allowed_users(allowed_roles=['COUNSELOR'])
    def update(self, request, *args, **kwargs):
      
        instance = self.queryset.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'Counselor schedule does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        if request.data['start_time'] > request.data['end_time']:
            return Response({'message': 'Start time cannot be greater than end time'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Counselor schedule updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Counselor Schedule Status",
                value={
                    "status": "string",
                },
                request_only=True,
            )
        ],
    )
    @allowed_users(allowed_roles=['ADMIN'])
    def update_status(self, request, *args, **kwargs):
      
        instance = self.queryset.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'Counselor schedule does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            schedule_obj = serializer.save()
            subject = 'Mental Well'
            message = f'Your schedule for {schedule_obj.day} was {schedule_obj.status}.'
            send_email(schedule_obj.counselor.user.id, subject, message, None)
            return Response({'message': 'Counselor schedule status updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(parameters=set_query_params('list', [
        {"name": 'counselor_id', "description": 'Filter by counselor_id'},
    ]))
    @allowed_users(allowed_roles=['ADMIN'])
    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        counselor_id = request.query_params.get('counselor_id', None)
        if counselor_id:
            queryset = queryset.filter(counselor=counselor_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @allowed_users(allowed_roles=['COUNSELOR'])
    def get_schedule(self, request, *args, **kwargs):
        queryset = self.queryset.filter(counselor=request.user.id)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
     
    @allowed_users(allowed_roles=['ADMIN', 'COUNSELOR'])
    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=request.user.id).first()
        if not obj:
            return Response({'message': 'Counselor schedule does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@extend_schema(tags=['Appointment Request'])
class AppointmentRequestViewSet(ModelViewSet):
    model_class = AppointmentRequest
    serializer_class = AppointmentRequestSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    @extend_schema(
        examples=[
            OpenApiExample(
                "Create Appointment Request",
                value={
                    "counselor": "string",
                    "schedule": "string",
                    "booking_date": "string",
                },
                request_only=True,
            )
        ]
    )
    @transaction.atomic()
    @allowed_users(allowed_roles=['CLIENT'])
    def create(self, request, *args, **kwargs):
        data = request.data
        counselor_instance = CounselorProfileModel.objects.filter(user__id=data['counselor'], user__user_role='COUNSELOR').first()
        if not counselor_instance:
            return Response({'message': 'Invalid Counselor'}, status=status.HTTP_400_BAD_REQUEST)
        
        client_instance = ClientProfileModel.objects.filter(user__id=request.user.id, user__user_role='CLIENT').first()
        if not client_instance:
            return Response({'message': 'Invalid Client'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            data['client']=request.user.id

        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Appointment Request created succesfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Appointment Request",
                value={
                    "counselor": "string",
                    "schedule": "string",
                    "booking_date": "string",
                },
                request_only=True,
            )
        ],
    )
    @transaction.atomic()
    @allowed_users(allowed_roles=['CLIENT'])
    def update(self, request, *args, **kwargs):
      
        instance = self.queryset.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'Appointment Request does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Appointment Request updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Appointment Request Status",
                value={
                    "status": "string",
                },
                request_only=True,
            )
        ],
    )
    @allowed_users(allowed_roles=['ADMIN'])
    def update_status(self, request, *args, **kwargs):
      
        instance = self.queryset.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'Appointment Request does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        if request.data['status'] == 'CONFIRMED':
            payment_instance = {
                'counselor': instance.counselor,
                'client': instance.client,
                'appointment': instance.id,
                'due_amount': instance.counselor.user.pay_per_session,
            }
            payment_serializer = PaymentSerializer(data=payment_instance)
            if payment_serializer.is_valid(raise_exception=True):
                payment_serializer.save()
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            appointment_obj = serializer.save()
            subject = 'Mental Well'
            message = f'Your appointment request on {appointment_obj.schedule.day} was {appointment_obj.status}.'
            send_email(appointment_obj.client.user.id, subject, message, None)
            return Response({'message': 'Appointment Request status updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(parameters=set_query_params('list', [
        {"name": 'counselor_id', "description": 'Filter by counselor_id'},
    ]))
    @allowed_users(allowed_roles=['ADMIN'])
    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        counselor_id = request.query_params.get('counselor_id', None)
        if counselor_id:
            queryset = queryset.filter(counselor=counselor_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @allowed_users(allowed_roles=['COUNSELOR'])
    def get_request(self, request, *args, **kwargs):
        queryset = self.queryset.filter(counselor=request.user.id, status='CONFIRMED')
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
     
    @allowed_users(allowed_roles=['ADMIN', 'COUNSELOR'])
    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=request.user.id).first()
        if not obj:
            return Response({'message': 'Appointment Request does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(tags=['Client Progress'])
class ClientProgressViewSet(ModelViewSet):
    model_class = ClientProgress
    serializer_class = ClientProgressSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    @extend_schema(
        examples=[
            OpenApiExample(
                "Create Client Progress",
                value={
                    "client": "string",
                    "status": "string",
                },
                request_only=True,
            )
        ]
    )
    @transaction.atomic()
    @allowed_users(allowed_roles=['COUNSELOR'])
    def create(self, request, *args, **kwargs):
        data = request.data
        counselor_instance = CounselorProfileModel.objects.filter(user__id=request.user.id, user__user_role='COUNSELOR').first()
        if not counselor_instance:
            return Response({'message': 'Invalid Counselor'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            data['counselor']=request.user.id
        
        client_instance = ClientProfileModel.objects.filter(user__id=data['client'], user__user_role='CLIENT').first()
        if not client_instance:
            return Response({'message': 'Invalid Client'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Client Progress created succesfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Client Progress",
                value={
                    "status": "string",
                },
                request_only=True,
            )
        ],
    )
    @transaction.atomic()
    @allowed_users(allowed_roles=['COUNSELOR'])
    def update(self, request, *args, **kwargs):
      
        instance = self.queryset.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'Client Progress does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Client Progress updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @extend_schema(parameters=set_query_params('list', [
        {"name": 'status', "description": 'Filter by client progress status'},
    ]))
    @allowed_users(allowed_roles=['COUNSELOR'])
    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        status = request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @allowed_users(allowed_roles=['COUNSELOR'])
    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=request.user.id).first()
        if not obj:
            return Response({'message': 'Client Progress does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@extend_schema(tags=['Client Progress Details'])
class ClientProgressDetailsViewSet(ModelViewSet):
    model_class = ClientProgressDetails
    serializer_class = ClientProgressDetailsSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    @extend_schema(
        examples=[
            OpenApiExample(
                "Create Client Progress Details",
                value={
                    "progress": "string",
                    "appointment": "string",
                    "details": "string",
                },
                request_only=True,
            )
        ]
    )
    @transaction.atomic()
    @allowed_users(allowed_roles=['COUNSELOR'])
    def create(self, request, *args, **kwargs):
        data = request.data
        counselor_instance = CounselorProfileModel.objects.filter(user__id=request.user.id, user__user_role='COUNSELOR').first()
        if not counselor_instance:
            return Response({'message': 'Invalid Counselor'}, status=status.HTTP_400_BAD_REQUEST)
        
        progress_instance = ClientProgress.objects.filter(id=data['progress']).first()
        if not progress_instance:
            return Response({'message': 'Invalid Client Progress'}, status=status.HTTP_400_BAD_REQUEST)
        
        appointment_instance = AppointmentRequest.objects.filter(id=data['appointment']).first()
        if not appointment_instance:
            return Response({'message': 'Invalid Appointment Request'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Client Progress Details created succesfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Client Progress Details",
                value={
                    "details": "string",
                },
                request_only=True,
            )
        ],
    )
    @transaction.atomic()
    @allowed_users(allowed_roles=['COUNSELOR'])
    def update(self, request, *args, **kwargs):
      
        instance = self.queryset.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'Client Progress Details does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Client Progress Details updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @extend_schema(parameters=set_query_params('list', [
        {"name": 'client_progress', "description": 'Filter by client progress'},
    ]))
    @allowed_users(allowed_roles=['COUNSELOR'])
    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        progress = request.query_params.get('client_progress', None)
        if progress:
            queryset = queryset.filter(progress=progress)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @allowed_users(allowed_roles=['COUNSELOR'])
    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=request.user.id).first()
        if not obj:
            return Response({'message': 'Client Progress Details does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@extend_schema(tags=['Achievements'])
class AchievementsViewSet(ModelViewSet):
    model_class = Achievements
    serializer_class = AchievementsSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    @extend_schema(
        examples=[
            OpenApiExample(
                "Create Achievements",
                value={
                    "title": "string",
                    "awarded_by": "string",
                    "date": "string",
                    "details": "string",
                },
                request_only=True,
            )
        ]
    )
    @transaction.atomic()
    @allowed_users(allowed_roles=['COUNSELOR'])
    def create(self, request, *args, **kwargs):
        data = request.data
        counselor_instance = CounselorProfileModel.objects.filter(user__id=request.user.id, user__user_role='COUNSELOR').first()
        if not counselor_instance:
            return Response({'message': 'Invalid Counselor'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            data['counselor']=request.user.id

        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Achievement added succesfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Achievement",
                value={
                    "title": "string",
                    "awarded_by": "string",
                    "date": "string",
                    "details": "string",
                },
                request_only=True,
            )
        ],
    )
    @transaction.atomic()
    @allowed_users(allowed_roles=['COUNSELOR'])
    def update(self, request, *args, **kwargs):
      
        instance = self.queryset.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'Achievement does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Achievement updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Achievement Status",
                value={
                    "status": "string",
                },
                request_only=True,
            )
        ],
    )
    @allowed_users(allowed_roles=['ADMIN'])
    def update_status(self, request, *args, **kwargs):
      
        instance = self.queryset.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'Achievement does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Achievement status updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @extend_schema(parameters=set_query_params('list', [
        {"name": 'counselor_id', "description": 'Filter by counselor_id'},
    ]))
    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        counselor_id = request.query_params.get('counselor_id', None)
        if counselor_id:
            queryset = queryset.filter(counselor=counselor_id, status="APPROVED")
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=request.user.id).first()
        if not obj:
            return Response({'message': 'Achievement does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@extend_schema(tags=['Article'])
class ArticleViewSet(ModelViewSet):
    model_class = Article
    serializer_class = ArticleSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    @extend_schema(
        examples=[
            OpenApiExample(
                "Create Article",
                value={
                    "image": "string",
                    "title": "string",
                    "article_file": "string",
                    "published_at": "string",
                },
                request_only=True,
            )
        ]
    )
    @transaction.atomic()
    @allowed_users(allowed_roles=['COUNSELOR'])
    def create(self, request, *args, **kwargs):
        data = request.data
        counselor_instance = CounselorProfileModel.objects.filter(user__id=request.user.id, user__user_role='COUNSELOR').first()
        if not counselor_instance:
            return Response({'message': 'Invalid Counselor'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            data['author']=request.user.id
            data['author_name']=f"{request.user.first_name if request.user.first_name else ''} {request.user.last_name if request.user.last_name else ''}"

        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Article created succesfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Article",
                value={
                    "image": "string",
                    "title": "string",
                    "article_file": "string",
                    "published_at": "string",
                },
                request_only=True,
            )
        ],
    )
    @transaction.atomic()
    @allowed_users(allowed_roles=['COUNSELOR'])
    def update(self, request, *args, **kwargs):
      
        instance = self.queryset.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'Article does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Article updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Article Status",
                value={
                    "status": "string",
                    "is_published": "string",
                },
                request_only=True,
            )
        ],
    )
    @allowed_users(allowed_roles=['ADMIN'])
    def update_status(self, request, *args, **kwargs):
      
        instance = self.queryset.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'Article does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Article status updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @extend_schema(parameters=set_query_params('list', [
        {"name": 'counselor_id', "description": 'Filter by counselor_id'},
    ]))
    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        counselor_id = request.query_params.get('counselor_id', None)
        if counselor_id:
            queryset = queryset.filter(counselor=counselor_id, is_published=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=request.user.id).first()
        if not obj:
            return Response({'message': 'Article does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@extend_schema(tags=['Video Journal'])
class VideoJournalViewSet(ModelViewSet):
    model_class = VideoJournal
    serializer_class = VideoJournalSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    @extend_schema(
        examples=[
            OpenApiExample(
                "Create Video Journal",
                value={
                    "image": "string",
                    "title": "string",
                    "video_link": "string",
                    "published_at": "string",
                },
                request_only=True,
            )
        ]
    )
    @transaction.atomic()
    @allowed_users(allowed_roles=['COUNSELOR'])
    def create(self, request, *args, **kwargs):
        data = request.data
        counselor_instance = CounselorProfileModel.objects.filter(user__id=request.user.id, user__user_role='COUNSELOR').first()
        if not counselor_instance:
            return Response({'message': 'Invalid Counselor'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            data['author']=request.user.id
            data['author_name']=f"{request.user.first_name if request.user.first_name else ''} {request.user.last_name if request.user.last_name else ''}"

        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Video Journal created succesfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Video Journal",
                value={
                     "image": "string",
                    "title": "string",
                    "video_link": "string",
                    "published_at": "string",
                },
                request_only=True,
            )
        ],
    )
    @transaction.atomic()
    @allowed_users(allowed_roles=['COUNSELOR'])
    def update(self, request, *args, **kwargs):
      
        instance = self.queryset.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'Video Journal does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Video Journal updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Video Journal Status",
                value={
                    "status": "string",
                    "is_published": "string",
                },
                request_only=True,
            )
        ],
    )
    @allowed_users(allowed_roles=['ADMIN'])
    def update_status(self, request, *args, **kwargs):
      
        instance = self.queryset.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'Video Journal does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Video Journal status updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @extend_schema(parameters=set_query_params('list', [
        {"name": 'counselor_id', "description": 'Filter by counselor_id'},
    ]))
    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        counselor_id = request.query_params.get('counselor_id', None)
        if counselor_id:
            queryset = queryset.filter(counselor=counselor_id, is_published=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=request.user.id).first()
        if not obj:
            return Response({'message': 'Video Journal does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@extend_schema(tags=['FAQ'])
class FAQViewSet(ModelViewSet):
    model_class = FAQModel
    serializer_class = FAQSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    @extend_schema(
        examples=[
            OpenApiExample(
                "Create FAQ",
                value={
                    "question": "string",
                },
                request_only=True,
            )
        ]
    )
    @transaction.atomic()
    @allowed_users(allowed_roles=['CLIENT'])
    def create(self, request, *args, **kwargs):
        instance = ClientProfileModel.objects.filter(user__id=request.user.id).first()
        if not instance:
            return Response({'message': 'Invalid Client'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            request.data['client'] = request.user.id

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'FAQ created succesfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @extend_schema(
        examples=[
            OpenApiExample(
               "Update FAQ Status",
                value={
                    "answer": "string",
                    "is_published": "string",
                },
                request_only=True,
            )
        ],
    )
    @allowed_users(allowed_roles=['ADMIN'])
    def update_status(self, request, *args, **kwargs):
      
        instance = self.queryset.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'FAQ does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'FAQ answered successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(is_published=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=request.user.id).first()
        if not obj:
            return Response({'message': 'FAQ does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@extend_schema(tags=['Review'])
class ReviewViewSet(ModelViewSet):
    model_class = Review
    serializer_class = ReviewSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'

    @extend_schema(
        examples=[
            OpenApiExample(
                "Create Review",
                value={
                    "counselor": "string",
                    "rating": 5,
                    "review_text": "string",
                },
                request_only=True,
            )
        ]
    )
    @transaction.atomic()
    @allowed_users(allowed_roles=['CLIENT'])
    def create(self, request, *args, **kwargs):
        instance = ClientProfileModel.objects.filter(user__id=request.user.id).first()
        if not instance:
            return Response({'message': 'Invalid Client'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            request.data['client'] = request.user.id

        appointment_qs = AppointmentRequest.objects.filter(client=request.user.id, status='DONE')
        request.data['appointment_count'] = appointment_qs.count()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Review created succesfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Review Status",
                value={
                    "status": "string",
                    "is_published": "string",
                },
                request_only=True,
            )
        ],
    )
    @allowed_users(allowed_roles=['ADMIN'])
    def update_status(self, request, *args, **kwargs):
      
        instance = self.queryset.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'Review does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Review updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(is_published=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=request.user.id).first()
        if not obj:
            return Response({'message': 'Review does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@extend_schema(tags=['Payment'])
class PaymentViewSet(ModelViewSet):
    model_class = Payment
    serializer_class = PaymentSerializer
    queryset = model_class.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_classes = CustomPagination
    lookup_field = 'id'
        
    @extend_schema(
        examples=[
            OpenApiExample(
               "Update Payment",
                value={
                    "paid_amount": "string",
                    "payment_method": "string",
                    "payment_date": "string",
                },
                request_only=True,
            )
        ],
    )
    @allowed_users(allowed_roles=['CLIENT'])
    def update(self, request, *args, **kwargs):
      
        instance = self.queryset.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'Payment instance does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        

        # Get the last 4 digits of the phone number
        last_4_digits = request.user.phone_number[-4:]
    
        # Generate a UUID and get the first 5 characters
        unique_id = request.user.id[:5]
    
        # Get the current timestamp in milliseconds
        timestamp = int(time.time() * 1000)
    
        # Construct the transaction ID
        request.data['transaction_id'] = f"#{last_4_digits}{unique_id}{timestamp}"

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            payment_obj = serializer.save()
            subject = 'Mental Well'
            message = f'Your payment of {payment_obj.due_amount} was successful.'
            send_email(None, subject, message, request.user.id)
            print(request.data['transaction_id'])
            return Response({'message': 'Payment updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @extend_schema(parameters=set_query_params('list', [
        {"name": 'counselor_id', "description": 'Filter by counselor_id'},
        {"name": 'client_id', "description": 'Filter by client_id'},

    ]))
    @allowed_users(allowed_roles=['ADMIN'])
    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        counselor_id = request.query_params.get('counselor_id', None)
        client_id = request.query_params.get('client_id', None)
        if counselor_id:
            queryset = queryset.filter(counselor=counselor_id)
        elif client_id:
            queryset = queryset.filter(client=client_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @extend_schema(parameters=set_query_params('list', [
        {"name": 'client_id', "description": 'Filter by client_id'},

    ]))
    @allowed_users(allowed_roles=['COUNSELOR'])
    def get_counselor_payment_history(self, request, *args, **kwargs):
        queryset = self.queryset.filter(counselor=request.user.id)
        client_id = request.query_params.get('client_id', None)
        if client_id:
            queryset = queryset.filter(client=client_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @allowed_users(allowed_roles=['CLIENT'])
    def get_client_payment_history(self, request, *args, **kwargs):
        queryset = self.queryset.filter(client=request.user.id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset
        obj = queryset.filter(id=request.user.id).first()
        if not obj:
            return Response({'message': 'Payment does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
