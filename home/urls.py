from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('posts', views.post, name='posts'),
    path('pages', views.page, name='pages'),
    path('data', views.data, name='data'),
    path('api/', include('home.api.urls')),
    path('users/', views.list_accounts, name='users'),
    path('start-virtual-browser/', views.start_virtual_browser, name='start_virtual_browser'),
]
