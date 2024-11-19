from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('posts', views.post, name='posts'),
    path('run-crawl/', views.run_crawl, name='run_crawl'),
    path('api/posts/', views.api_posts, name='api_posts'),
]
