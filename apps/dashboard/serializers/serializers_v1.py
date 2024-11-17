from rest_framework.serializers import *
from apps.dashboard.models import *

exclude_list = [
    'is_active',
    'created_at',
    'updated_at'
]


class BannerSerializer(ModelSerializer):
    
    class Meta:
        model = BannerModel
        exclude = exclude_list

class MotivationSerializer(ModelSerializer):
    
    class Meta:
        model = MotivationModel
        exclude = exclude_list

class ResourcesSerializer(ModelSerializer):
    
    class Meta:
        model = Resources
        exclude = exclude_list

class LegalDocumentSerializer(ModelSerializer):
    
    class Meta:
        model = LegalDocument
        exclude = exclude_list

class PrivacyPolicySerializer(ModelSerializer):
    
    class Meta:
        model = PrivacyPolicy
        exclude = exclude_list

class AboutUsSerializer(ModelSerializer):
    
    class Meta:
        model = AboutUs
        exclude = exclude_list

class FooterSerializer(ModelSerializer):
    
    class Meta:
        model = FooterModel
        exclude = exclude_list

class CounselorScheduleSerializer(ModelSerializer):

    class Meta:
        model = CounselorSchedule
        exclude = exclude_list

class AppointmentRequestSerializer(ModelSerializer):

    class Meta:
        model = AppointmentRequest
        exclude = exclude_list

class ClientProgressSerializer(ModelSerializer):

    class Meta:
        model = ClientProgress
        exclude = exclude_list

class ClientProgressDetailsSerializer(ModelSerializer):

    class Meta:
        model = ClientProgressDetails
        exclude = exclude_list

class AchievementsSerializer(ModelSerializer):

    class Meta:
        model = Achievements
        exclude = exclude_list

class ArticleSerializer(ModelSerializer):

    class Meta:
        model = Article
        exclude = exclude_list

class VideoJournalSerializer(ModelSerializer):

    class Meta:
        model = VideoJournal
        exclude = exclude_list

class FAQSerializer(ModelSerializer):

    class Meta:
        model = FAQModel
        exclude = exclude_list

class PaymentSerializer(ModelSerializer):

    class Meta:
        model = Payment
        exclude = exclude_list

class ReviewSerializer(ModelSerializer):

    class Meta:
        model = Review
        exclude = exclude_list