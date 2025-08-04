import datetime
from django.conf import settings

def blog_settings(request):
    return {
        'BLOG_NAME': settings.BLOG_NAME,
        'BLOG_DESCRIPTION': settings.BLOG_DESCRIPTION,
        'YEAR': datetime.datetime.now().year,
    }