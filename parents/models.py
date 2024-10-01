from parents.managers import ParentManager

from hitcount.models import HitCountMixin
from utilities.mixins import PersonModelMixin
from django.utils.translation import gettext_lazy as _


class Parent(PersonModelMixin, HitCountMixin):
    """
    Parents model (base fields are defined in the mixin)
    """

    # define other fields here

    objects = ParentManager() # overriding the default manager so we can adjust querysets dynamically

    class Meta:
        verbose_name = _("Parent")
        verbose_name_plural = _("Parents")
        ordering = ["-created_on", "first_name", "last_name", "gender", "age", "country"]

    def __str__(self) -> str:
        return self.full_name # from the mixin
