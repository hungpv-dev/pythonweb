from rest_framework import serializers
from ..models import Post, Page
from ..models import Post, User

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        
class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    def createUser(self, validated_data):
        return User.objects.create(**validated_data)
    
    def updateUser(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.link = validated_data.get('link', instance.link)
        instance.cookie = validated_data.get('cookie', instance.cookie)
        
        instance.save()
        return instance
