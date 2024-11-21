from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.views_list_accounts import UserViewSet
from . import views
from .views.posts import PostViewSet
from .views.pages import PaegViewSet 

router = DefaultRouter()
router.register(r'posts', PostViewSet)
<<<<<<< HEAD
router.register(r'users', UserViewSet)
=======
router.register(r'pages', PaegViewSet)
>>>>>>> 09204c59294ea50d82395f6f6bf550de0e981b86

urlpatterns = [
    path('', include(router.urls)),
]