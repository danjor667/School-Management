from django.apps import AppConfig


class TenantUsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tenant_users'


    def ready(self):
        import tenant_users.signals