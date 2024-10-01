from django.db import models

from accounts.managers import UserManager


class TenantUserManager(UserManager):
    def create_tenant_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
