from rest_framework import serializers
from blog_generator.models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):

    days_since_created = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        exclude = ['created_at', 'updated_at', 'transcript']


    def get_days_since_created(self, obj):
        from django.utils import timezone
        delta = timezone.now() - obj.created_at
        return delta.days