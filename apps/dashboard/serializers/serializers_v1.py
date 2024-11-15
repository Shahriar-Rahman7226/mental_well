from rest_framework import serializers
from ..models import Review, Article, VideoJournal

class ReviewSerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField()  #  the client's username 
    class Meta:
        model = Review
        fields = ['id', 'client', 'counselor_name', 'rating', 'review_text', 'created_at']


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()  # Display the author's username
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'author', 'content', 'published_at', 'updated_at']


class VlogSerializer(serializers.ModelSerializer):
    posted_by = serializers.StringRelatedField()  # Display the user's username who posted the vlog
    
    class Meta:
        model = Vlog
        fields = ['id', 'title', 'video_url', 'description', 'posted_by', 'posted_at']