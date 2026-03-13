from django.shortcuts import render
from django.views import generic
from apps.blog.models import Post


class HomeView(generic.ListView):
    model = Post
    context_object_name = 'posts'
    template_name = "blog/home.html"


def about(request):
    return render(request, 'blog/about.html')
# {% url 'post-detail' post.id %} {% url 'user-posts' post.author.username %}