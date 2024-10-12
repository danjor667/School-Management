from django.db import models
from teachers.managers import TeacherManager

from hitcount.models import HitCountMixin

from tenant_users.models import TenantUser
from utilities.mixins import PersonModelMixin
from django.utils.translation import gettext_lazy as _



class Teacher(PersonModelMixin, HitCountMixin):
    """
    Teacher model (base fields are defined in the mixin)
    """
    user = models.OneToOneField(TenantUser, on_delete=models.CASCADE)

    # define other fields here

    objects = TeacherManager() # overriding the default manager so we can adjust querysets dynamically

    class Meta:
        verbose_name = _("Enseignant(e)")
        verbose_name_plural = _("Enseignant(e)s")
        ordering = ["-created_on", "first_name", "last_name", "gender", "age", "country"]

    def __str__(self) -> str:
        return self.full_name # from the mixin
