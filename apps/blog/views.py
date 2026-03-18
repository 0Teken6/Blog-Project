from django.shortcuts import render, get_object_or_404
from django.views import generic
from apps.blog.models import Post, Category, Tag
from django.contrib.auth import get_user_model
from .filters import PostFilter, PostCustomFilter
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count


def home(request):
    context = {'posts': Post.objects.all().order_by('-created_at')}
    context["categories"] = Category.objects.annotate(post_count=Count("posts"))
    context["tags"] = Tag.objects.annotate(post_count=Count("posts"))
    return render(request, 'blog/home.html', context=context)


def about(request):
    return render(request, 'blog/about.html')


class PostListView(FilterView):
    model = Post
    context_object_name = 'posts'
    template_name = "blog/posts.html"
    ordering = ['-created_at']
    filterset_class = PostFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categories"] = Category.objects.annotate(post_count=Count("posts"))
        context["tags"] = Tag.objects.annotate(post_count=Count("posts"))

        return context


class PostDetailView(generic.DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/post_detail.html'


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    context_object_name = 'post'
    fields = ['title', 'content', 'category', 'tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        if self.get_object().author == self.request.user:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Post
    success_url = 'home'
    template_name = 'post_delete.html'

    def test_func(self):
        if self.get_object().author == self.request:
            return True
        return False


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ['title', 'content', 'category', 'tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UserPostListView(FilterView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/user_posts.html'
    ordering = ['-created_at']
    filterset_class = PostCustomFilter


    def get_queryset(self):
        user = get_object_or_404(get_user_model(), username=self.kwargs.get('username'))
        return Post.objects.filter(author=user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.kwargs.get('username')
        context["categories"] = Category.objects.annotate(post_count=Count("posts"))
        context["tags"] = Tag.objects.annotate(post_count=Count("posts"))
        return context
