from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import BlogPostSerializer
from blog_generator.models import BlogPost
# Create your views here.


@api_view(['GET'])
def blog_list(request):
    """
    GET: List all blogs
    POST: Generate a new blog
    """

    if request.method == 'GET':
        blogs = BlogPost.objects.all()
        serializer = BlogPostSerializer(blogs, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
def blog_details(request, pk):
    """
    GET: Retrieve a blog
    """
    try:
        blog = BlogPost.objects.get(pk=pk)
    except BlogPost.DoesNotExist:
        return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = BlogPostSerializer(blog)
        return Response(serializer.data)
