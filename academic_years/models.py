import uuid
from django.db import models
from accounts.models import User
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class AcademicYear(models.Model):
    added_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, verbose_name=_("Ajoutée en ligne par"), editable=False)
    year = models.CharField(max_length=500, verbose_name=_("Année"), help_text=_("Ex: 2024 - 2025"))
    details = models.TextField(null=True, blank=True, verbose_name=_("Plus de détails"),
        help_text=_("Si vous voulez donner plus de détails sur cette année académique"))
    slug = models.SlugField(max_length=500, verbose_name=_("Lien d'accès"), null=True, blank=True, editable=False)
    uuid = models.UUIDField(default=uuid.uuid4, null=True, blank=True, unique=True, editable=False, verbose_name="UUID")
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Ajouté le"))
    updated_on = models.DateTimeField(auto_now=True, verbose_name=_("Modifié le"))
    extra_data = models.JSONField(null=True, blank=True, verbose_name=_("Données supplémentaires"))
    
    class Meta:
        verbose_name = _("Année scolaire")
        verbose_name_plural = _("Années scolaires")
        ordering = ["-date", "year"]
    
    def __str__(self) -> str:
        return self.year
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.year)
        super(AcademicYear, self).save(*args, **kwargs)
