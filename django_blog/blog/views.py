from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q, Count
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from admin_panel.models import Post, Tag, User, Comment, Subscriber
from .forms import CommentForm, SubscribeForm


class PostListView(ListView):
    """Homepage view showing published posts"""
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        return Post.objects.filter(status='published').select_related('author').prefetch_related('tags')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_posts'] = Post.objects.filter(
            status='published'
        ).order_by('-views')[:3]
        context['recent_posts'] = Post.objects.filter(
            status='published'
        ).order_by('-published_at')[:5]
        context['popular_tags'] = Tag.objects.annotate(
            post_count=Count('posts')
        ).filter(post_count__gt=0).order_by('-post_count')[:10]
        return context


class PostDetailView(DetailView):
    """Individual post detail view"""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        return Post.objects.filter(status='published').select_related('author').prefetch_related('tags')
    
    def get_object(self):
        post = super().get_object()
        # Increment view count
        post.views += 1
        post.save(update_fields=['views'])
        return post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['comments'] = post.comments.filter(approved=True).order_by('created_at')
        context['comment_form'] = CommentForm()
        context['related_posts'] = Post.objects.filter(
            tags__in=post.tags.all(),
            status='published'
        ).exclude(id=post.id).distinct()[:3]
        return context


class AuthorPostsView(ListView):
    """View showing posts by a specific author"""
    model = Post
    template_name = 'blog/author_posts.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        self.author = get_object_or_404(User, id=self.kwargs['author_id'])
        return Post.objects.filter(
            author=self.author,
            status='published'
        ).select_related('author').prefetch_related('tags')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.author
        return context


class TagPostsView(ListView):
    """View showing posts with a specific tag"""
    model = Post
    template_name = 'blog/tag_posts.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Post.objects.filter(
            tags=self.tag,
            status='published'
        ).select_related('author').prefetch_related('tags')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


class SearchView(ListView):
    """Search view for posts"""
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query) | 
                Q(excerpt__icontains=query),
                status='published'
            ).select_related('author').prefetch_related('tags')
        return Post.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class SubscribeView(View):
    """AJAX view for newsletter subscription"""
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request):
        form = SubscribeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subscriber, created = Subscriber.objects.get_or_create(email=email)
            if created:
                return JsonResponse({
                    'success': True,
                    'message': 'Successfully subscribed to our newsletter!'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'You are already subscribed!'
                })
        return JsonResponse({
            'success': False,
            'message': 'Please enter a valid email address.'
        })


class CommentCreateView(View):
    """AJAX view for creating comments"""
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            post_id = request.POST.get('post_id')
            comment.post = get_object_or_404(Post, id=post_id)
            comment.save()
            return JsonResponse({
                'success': True,
                'message': 'Your comment has been submitted and is awaiting approval.'
            })
        return JsonResponse({
            'success': False,
            'message': 'Please fill in all required fields correctly.'
        })