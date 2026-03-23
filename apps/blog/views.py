from django.shortcuts import render, get_object_or_404
from django.views import generic
from apps.blog.models import Post, Category, Tag
from django.contrib.auth import get_user_model
from .filters import PostFilter
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count


def home(request):
    posts = Post.objects.all().order_by('-created_at')
    filterset = PostFilter(request.GET, queryset=Post.objects.all())
    context = {'posts': posts, 'filterset': filterset}
    return render(request, 'blog/home.html', context=context)


def about(request):
    return render(request, 'blog/about.html')


class PostListView(generic.ListView):
    model = Post
    context_object_name = 'posts'
    template_name = "blog/posts.html"
    ordering = ['-created_at']
    paginate_by = 5


    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filterset"] = self.filterset
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


class UserPostListView(generic.ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/user_posts.html'
    ordering = ['-created_at']
    paginate_by = 5


    def get_queryset(self):
        user = get_object_or_404(get_user_model(), username=self.kwargs.get('username'))
        self.filterset = PostFilter(self.request.GET, queryset=Post.objects.filter(author=user))
        return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filterset"] = self.filterset
        context['username'] = self.kwargs.get('username')
        return context
