from rest_framework import serializers
from ..models import Post, User
from ..models import Post, Page

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
        instance.code = validated_data.get('code', instance.code)
        instance.name = validated_data.get('name', instance.name)
        instance.type = validated_data.get('type', instance.type)
        instance.link = validated_data.get('link', instance.link)
        instance.cookie = validated_data.get('cookie', instance.cookie)
        
        instance.save(update_fields=['code', 'name', 'type', 'link', 'cookie'])
        return instance
