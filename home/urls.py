from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('posts', views.post, name='posts'),
    path('api/', include('home.api.urls')),
    # path('run-crawl/', views.run_crawl, name='run_crawl'),
    # path('api/posts/', views.api_posts, name='api_posts'),
    # path('api/posts/<int:id>/', views.api_post_detail, name='api_post_detail'),
]
