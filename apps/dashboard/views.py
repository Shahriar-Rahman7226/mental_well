from django.shortcuts import render

from rest_framework import viewsets
from .models import Review
from .serializers import ReviewSerializer
from .models import Article
from .serializers import ArticleSerializer
from .models import Vlog
from .serializers import VlogSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer



class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer



class VlogViewSet(viewsets.ModelViewSet):
    queryset = Vlog.objects.all()
    serializer_class = VlogSerializer