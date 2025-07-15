from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.core.paginator import Paginator
from ..models import User
from ..forms import UserForm
from ..permissions import SuperuserRequiredMixin


class UserListView(LoginRequiredMixin, View):
    """List all users in admin panel"""
    template_name = 'admin_panel/users/list.html'
    login_url = '/admin-panel/login/'
    
    def get(self, request):
        users = User.objects.all().order_by('-date_joined')
        paginator = Paginator(users, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'users': page_obj,
            'page_obj': page_obj,
        }
        return render(request, self.template_name, context)


class UserCreateView(LoginRequiredMixin, SuperuserRequiredMixin, View):
    """Create new user"""
    template_name = 'admin_panel/users/create.html'
    form_class = UserForm
    login_url = '/admin-panel/login/'
    non_superuser_redirect_url = '/admin-panel/users/'
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'User created successfully!')
            return redirect('admin_panel:user_list')
        return render(request, self.template_name, {'form': form})


class UserUpdateView(LoginRequiredMixin, SuperuserRequiredMixin, View):
    """Update existing user"""
    template_name = 'admin_panel/users/update.html'
    form_class = UserForm
    login_url = '/admin-panel/login/'
    non_superuser_redirect_url = '/admin-panel/users/'
    
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = self.form_class(instance=user)
        return render(request, self.template_name, {'form': form, 'user_obj': user})
    
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = self.form_class(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'User updated successfully!')
            return redirect('admin_panel:user_list')
        return render(request, self.template_name, {'form': form, 'user_obj': user})


class UserDeleteView(LoginRequiredMixin, SuperuserRequiredMixin, View):
    """Delete user"""
    template_name = 'admin_panel/users/delete.html'
    login_url = '/admin-panel/login/'
    non_superuser_redirect_url = '/admin-panel/users/'
    
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        return render(request, self.template_name, {'user_obj': user})
    
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if user == request.user:
            messages.error(request, 'You cannot delete your own account!')
            return redirect('admin_panel:user_list')
        if request.user.is_superuser:
            messages.error(request, 'You cannot delete superuser account!')
            return redirect('admin_panel:user_list')
        user.delete()
        messages.success(request, 'User deleted successfully!')
        return redirect('admin_panel:user_list')