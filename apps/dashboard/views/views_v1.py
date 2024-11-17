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
    @transaction.atomic()
    @allowed_users(allowed_roles=['COUNSELOR'])
    def update(self, request, *args, **kwargs):
      
        instance = self.queryset.filter(id=kwargs['id']).first()

        if not instance:
            return Response({'message': 'Counselor schedule does not exists'}, status=status.HTTP_400_BAD_REQUEST)

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
            serializer.save()
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

        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
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
    
