from django.contrib import admin
from .models import BlogPost
# Register your models here.

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):

    readonly_fields = ('created_at', 'updated_at')
    