from django.db import models

class Post(models.Model):
    post_id = models.CharField(max_length=255, null=True, unique=True)
    link_facebook = models.TextField(null=True)
    page_id = models.IntegerField()
    content = models.TextField(null=True)
    media = models.JSONField(null=True)
    like = models.CharField(max_length=50, default='0')
    comment = models.CharField(max_length=50, default='0')
    share = models.CharField(max_length=50, default='0')
    up = models.BooleanField(default=False)
    link_up = models.TextField(null=True)
    user_id = models.IntegerField(default=0)
    page_up_id = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class Page(models.Model):
    link = models.CharField(max_length=155)
    type = models.CharField(max_length=55, null=True, default='Chủ đề')
    type_page = models.IntegerField(default=1)
    user_id = models.IntegerField(null=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)
    content = models.TextField()


class User(models.Model):
    name = models.IntegerField(null=True)
    link = models.CharField(max_length=155)
    cookie = models.JSONField(null=True)
