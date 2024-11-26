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
    up = models.IntegerField(default=0,db_comment='0: Chờ duyệt, 1: Đã duyệt, 2: Đã huỷ')
    link_up = models.TextField(null=True)
    user_id = models.IntegerField(default=0)
    page_up_id = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class Page(models.Model):
    link = models.CharField(max_length=155)
    type = models.CharField(max_length=55, null=True, default='Chủ đề')
    type_page = models.IntegerField(default=1, db_comment='1: Page lấy dữ liệu, 2: Page đăng bài')
    user_id = models.IntegerField(null=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)
    content = models.TextField()


class User(models.Model):
    name = models.CharField(null=True,max_length=155)
    code = models.CharField(null=True,max_length=155)
    pid = models.CharField(max_length=55, null=True)
    link = models.CharField(max_length=155)
    type = models.IntegerField(max_length=1, default=1, db_comment='1: User lấy dữ liệu, 2: User đăng bài')
    cookie = models.JSONField(null=True)

class PagePost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    status = models.IntegerField(max_length=1, default=1, db_comment='1: Chưa thực thi, 2: Đã thực thi')
    created_at = models.DateTimeField(auto_now_add=True)
