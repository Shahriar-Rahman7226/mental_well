from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE) 
    counselor_name = models.CharField(max_length=200)  
    rating = models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]) 
    review_text = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Review by {self.client.username} for {self.counselor_name}"

    class Meta:
        ordering = ['-created_at'] 

        


       class Article(models.Model):
    title = models.CharField(max_length=200) 
    author = models.ForeignKey(User, on_delete=models.CASCADE)  
    content = models.TextField()  # Full content of the article
    published_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_at'] 




        class Vlog(models.Model):
    title = models.CharField(max_length=200)  
    video_url = models.URLField()  
    description = models.TextField()  
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)  
    posted_at = models.DateTimeField(auto_now_add=True) 
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-posted_at'] 