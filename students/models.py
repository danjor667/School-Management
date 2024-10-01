from students.managers import StudentManager

from django.db import models
from hitcount.models import HitCountMixin
from utilities.mixins import PersonModelMixin
from django.utils.translation import gettext_lazy as _



class Student(PersonModelMixin, HitCountMixin):
    """
    Student model (base fields are defined in the mixin)
    """

    # define other fields here
    registration_num = models.CharField(max_length=50, verbose_name=_("N° matricule"), null=True, blank=True)


    objects = StudentManager() # overriding the default manager so we can adjust querysets dynamically

    class Meta:
        verbose_name = _("Élève")
        verbose_name_plural = _("Élèves")
        ordering = ["-created_on", "first_name", "last_name", "gender", "age", "country"]

    def __str__(self) -> str:
        return self.full_name # from the mixin
