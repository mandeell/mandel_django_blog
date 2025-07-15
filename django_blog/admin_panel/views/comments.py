from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.core.paginator import Paginator
from ..models import Comment


class CommentListView(LoginRequiredMixin, View):
    """List all comments in admin panel"""
    template_name = 'admin_panel/comments/list.html'
    login_url = '/admin-panel/login/'
    
    def get(self, request):
        comments = Comment.objects.select_related('post').order_by('-created_at')
        paginator = Paginator(comments, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'comments': page_obj,
            'page_obj': page_obj,
        }
        return render(request, self.template_name, context)


class CommentApproveView(LoginRequiredMixin, View):
    """Approve/unapprove comment"""
    login_url = '/admin-panel/login/'
    
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.approved = not comment.approved
        comment.save()
        
        status = 'approved' if comment.approved else 'unapproved'
        messages.success(request, f'Comment {status} successfully!')
        return redirect('admin_panel:comment_list')


class CommentDeleteView(LoginRequiredMixin, View):
    """Delete comment"""
    template_name = 'admin_panel/comments/delete.html'
    login_url = '/admin-panel/login/'
    
    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        return render(request, self.template_name, {'comment': comment})
    
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        messages.success(request, 'Comment deleted successfully!')
        return redirect('admin_panel:comment_list')