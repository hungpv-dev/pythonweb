from rest_framework import serializers
from ..models import Post, Page

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        
class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = '__all__'