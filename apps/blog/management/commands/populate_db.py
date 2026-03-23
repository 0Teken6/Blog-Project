import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import lorem_ipsum
from apps.blog.models import Post, Category, Tag
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Creates application data'

    def handle(self, *args, **kwargs):
        # get or create superuser
        user = get_user_model().objects.filter(username='admin').first()
        if not user:
            user = get_user_model().objects.create_superuser(username='admin', password='test')
        
        categories = [
            Category(name='Sport'),
            Category(name='News'),
        ]

        Category.objects.bulk_create(categories)
        categories = Category.objects.all()

        posts = [
            Post(title="Why Python Is Still My Favorite Language", content=lorem_ipsum.paragraph(), author=user, category=categories.get(name='News')),
            Post(title="How Data Analytics is Transforming Football", content=lorem_ipsum.paragraph(), author=user, category=categories.get(name='Sport')),
            Post(title="The Science Behind Elite Athlete Performance", content=lorem_ipsum.paragraph(), author=user, category=categories.get(name='Sport')),
            Post(title="Training Smarter, Not Harder: Modern Fitness Methods", content=lorem_ipsum.paragraph(), author=user, category=categories.get(name='News')),
            Post(title="Future of Electric Cars", content=lorem_ipsum.paragraph(), author=user, category=categories.get(name='News')),
            Post(title="Why Morning Routines Matter", content=lorem_ipsum.paragraph(), author=user, category=categories.get(name='News')),
        ]

        Post.objects.bulk_create(posts)

