from django.contrib.auth.backends import ModelBackend

from django_tenants.utils import schema_context
from schools.models import School
from tenant_users.models import TenantUser


class TenantBackend(ModelBackend):
    tenants = School.objects.all()
    UserModel = TenantUser

    def authenticate(self, request, email=None, password=None, **kwargs):
        for tenant in self.tenants:
            if tenant.name != "School SAAS":
                with schema_context(tenant.schema_name):
                    user = TenantUser.objects.get(email=email)
                    if not user:
                        return None
                    if user.check_password(password):
                        setattr(user, "tenant", tenant)
                        return user


class DefaultBackend(ModelBackend):
    pass