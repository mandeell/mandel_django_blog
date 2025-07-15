from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
import re
from django.core.exceptions import ValidationError

def validate_strong_password(value):
    """ Ensure password has uppercase, lowercase, digits, symbols, and min length 8. """
    if len(value) < 8:
        raise ValidationError('Password must be at least 8 characters long.')
    if not re.search(r'[A-Z]', value):
        raise ValidationError('Password must contain at least one uppercase letter.')
    if not re.search(r'[a-z]', value):
        raise ValidationError('Password must contain at least one lowercase letter.')
    if not re.search(r'[0-9]', value):
        raise ValidationError('Password must contain at least one digit.')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise ValidationError('Password must contain at least one special character (e.g., !@#$%^&*).')


class SuperuserRequiredMixin(UserPassesTestMixin):
    """
    Restrict view access to superusers only. Redirects non-superusers to a custom URL. """
    non_superuser_redirect_url = '/admin-panel/'

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        """ Redirect non-superusers to the specified URL. """
        messages.error(self.request, 'You do not have permission to access this page')
        return redirect(self.non_superuser_redirect_url)