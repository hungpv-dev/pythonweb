from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.posts import PostViewSet
from .views.pages import PaegViewSet 

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'pages', PaegViewSet)

urlpatterns = [
    path('', include(router.urls)),
]