from django.contrib import admin
from .models import Post, Page, Comment, User

admin.site.register(Post)
admin.site.register(Page)
admin.site.register(Comment)
admin.site.register(User)