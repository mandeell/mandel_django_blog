from django.conf import settings
import time

def blog_settings(request):
    return {
        'BLOG_NAME': settings.BLOG_NAME,
        'BLOG_DESCRIPTION': settings.BLOG_DESCRIPTION,
        'YEAR': time.strftime('%Y'),
    }