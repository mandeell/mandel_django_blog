from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.urls import reverse_lazy
from ..forms import LoginForm
from ..models import User


class LoginView(View):
    """Admin login view using Django sessions"""
    template_name = 'admin_panel/login.html'
    form_class = LoginForm
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('admin_panel:dashboard')
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            if not User.objects.filter(username=username).exists():
                messages.error(request, 'No account found with this username.')
                return render(request, self.template_name, {'form': form})

            user = authenticate(request=request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('admin_panel:dashboard')
            else:
                messages.error(request, 'Invalid username of password.')
        else:
            messages.error(request, 'Please provide valid input.')
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    """Admin logout view"""
    
    def post(self, request):
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('admin_panel:login')
    
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('admin_panel:login')