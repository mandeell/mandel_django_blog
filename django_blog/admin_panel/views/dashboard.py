from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.db.models import Count, Q, Sum
from ..models import Post, Comment, User, Tag, Subscriber, Analytics


class DashboardView(LoginRequiredMixin, View):
    """Admin dashboard with analytics"""
    template_name = 'admin_panel/dashboard.html'
    login_url = '/admin-panel/login/'
    
    def get(self, request):
        # Optimized analytics with single queries using annotations
        post_stats = Post.objects.aggregate(
            total_posts=Count('id'),
            published_posts=Count('id', filter=Q(status='published')),
            total_views=Sum('views')
        )
        
        comment_stats = Comment.objects.aggregate(
            total_comments=Count('id'),
            pending_comments=Count('id', filter=Q(approved=False)),
            approved_comments=Count('id', filter=Q(approved=True))
        )
        
        subscriber_count = Subscriber.objects.filter(is_active=True).count()
        
        # Optimized posts by author with single query
        posts_by_author = (
            User.objects
            .annotate(post_count=Count('posts'))
            .filter(post_count__gt=0)
            .order_by('-post_count')[:5]
            .values('username', 'post_count')
        )
        
        # Optimized most commented posts
        most_commented = (
            Post.objects
            .annotate(comment_count=Count('comments', filter=Q(comments__approved=True)))
            .filter(comment_count__gt=0)
            .order_by('-comment_count')[:5]
            .select_related('author')
        )
        
        # Recent activity with optimized queries
        recent_posts = Post.objects.select_related('author').order_by('-created_at')[:5]
        recent_comments = Comment.objects.select_related('post').order_by('-created_at')[:5]
        
        context = {
            'total_posts': post_stats['total_posts'] or 0,
            'published_posts': post_stats['published_posts'] or 0,
            'total_views': post_stats['total_views'] or 0,
            'total_comments': comment_stats['total_comments'] or 0,
            'pending_comments': comment_stats['pending_comments'] or 0,
            'approved_comments': comment_stats['approved_comments'] or 0,
            'total_subscribers': subscriber_count,
            'posts_by_author': posts_by_author,
            'most_commented': most_commented,
            'recent_posts': recent_posts,
            'recent_comments': recent_comments,
        }
        return render(request, self.template_name, context)