import django_filters
from .models import Post, Category, Tag
from django import forms
from django.db.models import Count


class PostFilter(django_filters.FilterSet):
    category = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.annotate(post_count=Count("posts")),
        widget=forms.CheckboxSelectMultiple
    )

    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.annotate(post_count=Count("posts")),
        widget=forms.CheckboxSelectMultiple
    )
    
    class Meta:
        model = Post
        fields = ['category', 'tags']


class PostCustomFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = ('category', 'tags')