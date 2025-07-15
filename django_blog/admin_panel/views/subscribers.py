from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from ..models import Subscriber
from ..forms import EmailPostsForm


class SubscriberListView(LoginRequiredMixin, View):
    """List all subscribers in admin panel"""
    template_name = 'admin_panel/subscribers/list.html'
    login_url = '/admin-panel/login/'
    
    def get(self, request):
        subscribers = Subscriber.objects.all().order_by('-subscribed_at')
        paginator = Paginator(subscribers, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'subscribers': page_obj,
            'page_obj': page_obj,
        }
        return render(request, self.template_name, context)


class SubscriberDeleteView(LoginRequiredMixin, View):
    """Delete subscriber"""
    template_name = 'admin_panel/subscribers/delete.html'
    login_url = '/admin-panel/login/'
    
    def get(self, request, pk):
        subscriber = get_object_or_404(Subscriber, pk=pk)
        return render(request, self.template_name, {'subscriber': subscriber})
    
    def post(self, request, pk):
        subscriber = get_object_or_404(Subscriber, pk=pk)
        subscriber.delete()
        messages.success(request, 'Subscriber deleted successfully!')
        return redirect('admin_panel:subscriber_list')


class SubscriberEmailView(LoginRequiredMixin, View):
    """Send message to subscriber(s)"""
    template_name = 'admin_panel/subscribers/email.html'
    login_url = '/admin-panel/login/'

    def get(self, request, pk=None):
        subscriber = None
        if pk:
            subscriber = get_object_or_404(Subscriber, pk=pk)
        form = EmailPostsForm()
        return render(request, self.template_name, {'subscriber': subscriber, 'form': form})

    def post(self, request, pk=None):
        subscriber = None
        if pk:
            subscriber = get_object_or_404(Subscriber, pk=pk)
        
        form = EmailPostsForm(request.POST)
        if form.is_valid():
            posts = form.cleaned_data['posts']
            send_to_all = form.cleaned_data['send_to_all']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Get site information
            current_site = get_current_site(request)
            site_url = f"http://{current_site.domain}"
            
            # Determine recipients
            if send_to_all or not subscriber:
                recipients = list(Subscriber.objects.values_list('email', flat=True))
                recipient_count = len(recipients)
            else:
                recipients = [subscriber.email]
                recipient_count = 1

            if not recipients:
                messages.error(request, 'No subscribers found to send email to!')
                return render(request, self.template_name, {'subscriber': subscriber, 'form': form})

            # Send emails to each recipient individually for personalization
            success_count = 0
            failed_emails = []
            
            for recipient_email in recipients:
                try:
                    # Prepare context for email template
                    email_context = {
                        'subject': subject,
                        'message': message,
                        'posts': posts,
                        'site_url': site_url,
                        'blog_name': getattr(settings, 'BLOG_NAME', 'Django Blog'),
                        'recipient_email': recipient_email,
                    }
                    
                    # Render HTML email
                    html_content = render_to_string('emails/newsletter.html', email_context)
                    
                    # Render plain text email
                    text_content = render_to_string('emails/newsletter.txt', email_context)
                    
                    # Create email message
                    email = EmailMultiAlternatives(
                        subject=subject,
                        body=text_content,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[recipient_email]
                    )
                    
                    # Attach HTML version
                    email.attach_alternative(html_content, "text/html")
                    
                    # Send email
                    email.send(fail_silently=False)
                    success_count += 1
                    
                except Exception as e:
                    failed_emails.append(f"{recipient_email}: {str(e)}")
                    continue
            
            # Provide feedback to user
            if success_count > 0:
                messages.success(request, f'Newsletter sent successfully to {success_count} subscriber(s)!')
            
            if failed_emails:
                failed_count = len(failed_emails)
                messages.warning(request, f'Failed to send to {failed_count} subscriber(s). Check email configuration.')
                # Optionally log the failed emails for debugging
                print("Failed emails:", failed_emails)
            
            if success_count == 0:
                messages.error(request, 'Failed to send newsletter to any subscribers!')
                return render(request, self.template_name, {'subscriber': subscriber, 'form': form})
            
            return redirect('admin_panel:subscriber_list')
            
        else:
            # Form has errors
            return render(request, self.template_name, {'subscriber': subscriber, 'form': form})