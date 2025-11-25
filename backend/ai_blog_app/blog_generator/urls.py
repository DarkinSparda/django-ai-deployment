from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.user_signup, name='signup'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('generate-blog', views.generate_blog, name='generate-blog'),
    path('get-blog-by-uuid/<str:blog_uuid>', views.get_blog_by_uuid, name='get-blog-by-uuid'),
    path('blog-list', views.blog_list, name='blog-list'),
    path('blog-details/<int:id>', views.blog_details, name='blog-details'),
]