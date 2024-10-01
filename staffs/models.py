from staffs.managers import SchoolStaffManager

from hitcount.models import HitCountMixin
from utilities.mixins import PersonModelMixin
from django.utils.translation import gettext_lazy as _


class SchoolStaff(PersonModelMixin, HitCountMixin):
    """
    School staff model (base fields are defined in the mixin)
    """
    
    # define other fields here
    
    objects = SchoolStaffManager() # overriding the default manager so we can adjust querysets dynamically
    
    class Meta:
        verbose_name = _("Membre de l'administration")
        verbose_name_plural = _("Membres de l'administration")
        ordering = ["-created_on", "first_name", "last_name", "gender", "age", "country"]
    
    def __str__(self) -> str:
        return self.full_name # from the mixin
