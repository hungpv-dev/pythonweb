from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.views_list_accounts import UserViewSet
from . import views
from .views.posts import PostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]