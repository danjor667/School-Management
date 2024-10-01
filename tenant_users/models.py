from django.contrib.auth.models import Group, Permission, AbstractUser
from django.db import models
from accounts.models import User
from tenant_users.managers import TenantUserManager
from django.utils.translation import gettext_lazy as _


class TenantUser(AbstractUser):
    """ Tenant User model use to authenticate. Inherits from main User model """
    

    groups = models.ManyToManyField(
        Group,
        related_name='tenant_user_set',
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_query_name='tenant_user'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='tenant_user_permissions_set',  #
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_query_name='tenant_user_permissions'
    )

    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('username'), max_length=150, unique=True, blank=True, null=True)

    EMAIL_FIELD = None  # No need
    USERNAME_FIELD = "email"  # Can be an email, an username, a registration number, a phone number, ...
    REQUIRED_FIELDS = []

    objects = TenantUserManager()
    
    
    class Meta:
        verbose_name = _("Utilisateur")
        verbose_name_plural = _("Utilisateurs")
        ordering = ["-date_joined", "email", "first_name", "last_name"]
    
    @property
    def created_on(self):
        return self.date_joined
    
    @property
    def date(self):
        return self.date_joined
    
    @property
    def user_str_repr(self):
        pass
    
    
    # @property
    # def role_is_student(self):
    #     return self.role == TenantUser.RoleType.STUDENT
    #
    # @property
    # def role_is_teacher(self):
    #     return self.role == TenantUser.RoleType.TEACHER
    #
    # @property
    # def role_is_principal(self):
    #     return self.role == TenantUser.RoleType.PRINCIPAL
    #
    # @property
    # def role_is_school_staff(self):
    #     return self.role == TenantUser.RoleType.SCHOOL_STAFF
    #
    # @property
    # def role_is_parent(self):
    #     return self.role == TenantUser.RoleType.PARENT
    #
    # @property
    # def role_is_others(self):
    #     return self.role == TenantUser.RoleType.OTHERS
