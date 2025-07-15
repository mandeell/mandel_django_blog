from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.core.paginator import Paginator
from ..models import Post
from ..forms import PostForm


class PostListView(LoginRequiredMixin, View):
    """List all posts in admin panel"""
    template_name = 'admin_panel/posts/list.html'
    login_url = '/admin-panel/login/'
    
    def get(self, request):
        posts = Post.objects.select_related('author').prefetch_related('tags').order_by('-created_at')
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'posts': page_obj,
            'page_obj': page_obj,
        }
        return render(request, self.template_name, context)


class PostCreateView(LoginRequiredMixin, View):
    """Create new post"""
    template_name = 'admin_panel/posts/create.html'
    form_class = PostForm
    login_url = '/admin-panel/login/'
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, 'Post created successfully!')
            return redirect('admin_panel:post_list')
        return render(request, self.template_name, {'form': form})


class PostUpdateView(LoginRequiredMixin, View):
    """Update existing post"""
    template_name = 'admin_panel/posts/update.html'
    form_class = PostForm
    login_url = '/admin-panel/login/'
    
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = self.form_class(instance=post)
        return render(request, self.template_name, {'form': form, 'post': post})
    
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = self.form_class(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('admin_panel:post_list')
        return render(request, self.template_name, {'form': form, 'post': post})


class PostDeleteView(LoginRequiredMixin, View):
    """Delete post"""
    template_name = 'admin_panel/posts/delete.html'
    login_url = '/admin-panel/login/'
    
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        return render(request, self.template_name, {'post': post})
    
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('admin_panel:post_list')