from django.apps import AppConfig


class AdminPanelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_panel'
    
    def ready(self):
        # Import templatetags to ensure they are registered
        import admin_panel.templatetags.quill_tags
