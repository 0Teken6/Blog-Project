from django.contrib import admin
from apps.blog.models import Post, Category, Tag


admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)