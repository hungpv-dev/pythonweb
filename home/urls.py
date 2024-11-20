from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('posts', views.post, name='posts'),
    path('posts/<int:id>/', views.post_show, name='post_show'),
    path('run-crawl/', views.run_crawl, name='run_crawl'),
    path('api/posts/', views.api_posts, name='api_posts'),
    path('api/posts/<int:id>/', views.api_post_detail, name='api_post_detail'),
]
