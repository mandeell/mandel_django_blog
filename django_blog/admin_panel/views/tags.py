from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.core.paginator import Paginator
from ..models import Tag
from ..forms import TagForm


class TagListView(LoginRequiredMixin, View):
    """List all tags in admin panel"""
    template_name = 'admin_panel/tags/list.html'
    login_url = '/admin-panel/login/'
    
    def get(self, request):
        tags = Tag.objects.all().order_by('name')
        paginator = Paginator(tags, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'tags': page_obj,
            'page_obj': page_obj,
        }
        return render(request, self.template_name, context)


class TagCreateView(LoginRequiredMixin, View):
    """Create new tag"""
    template_name = 'admin_panel/tags/create.html'
    form_class = TagForm
    login_url = '/admin-panel/login/'
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tag created successfully!')
            return redirect('admin_panel:tag_list')
        return render(request, self.template_name, {'form': form})


class TagUpdateView(LoginRequiredMixin, View):
    """Update existing tag"""
    template_name = 'admin_panel/tags/update.html'
    form_class = TagForm
    login_url = '/admin-panel/login/'
    
    def get(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        form = self.form_class(instance=tag)
        return render(request, self.template_name, {'form': form, 'tag': tag})
    
    def post(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        form = self.form_class(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tag updated successfully!')
            return redirect('admin_panel:tag_list')
        return render(request, self.template_name, {'form': form, 'tag': tag})


class TagDeleteView(LoginRequiredMixin, View):
    """Delete tag"""
    template_name = 'admin_panel/tags/delete.html'
    login_url = '/admin-panel/login/'
    
    def get(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        return render(request, self.template_name, {'tag': tag})
    
    def post(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        tag.delete()
        messages.success(request, 'Tag deleted successfully!')
        return redirect('admin_panel:tag_list')