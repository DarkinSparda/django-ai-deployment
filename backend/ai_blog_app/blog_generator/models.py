from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    youtube_title = models.CharField(max_length=350)
    youtube_link = models.URLField()
    transcript = models.TextField()
    generated_content = models.TextField()
    model_used = models.CharField(null=True, blank=True, max_length=100)
    video_lang = models.CharField(max_length=50, null=True, blank=True)
    ARTICLE_SIZES = [('short', 'Short'), ('medium', 'Medium'), ('long', 'Long')]
    article_size = models.CharField(max_length=15, choices=ARTICLE_SIZES, default='medium', null=True, blank=True)
    time_to_generate = models.FloatField(null=True, blank=True, help_text="Time in seconds")
    time_to_summarize = models.FloatField(null=True, blank=True, help_text="Time in seconds")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.youtube_title} - ({self.article_size})"
    