import uuid, random, string
from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _
from django_tenants.models import TenantMixin, DomainMixin



class School(TenantMixin):
    """ Tenant Main Model """
    
    created_by = models.ForeignKey("accounts.User", on_delete=models.PROTECT, null=True, blank=True, editable=False,
        verbose_name=_("Admin ayant créé cette école"), related_name="created_companies")
    badge = models.CharField(max_length=500, verbose_name=_("Badge"), null=True, editable=False)
    slogan = models.CharField(max_length=25, verbose_name=_("Slogan"), null=True, blank=True, help_text=_("Le slogan de l'école"))
    name = models.CharField(max_length=100, verbose_name=_("Nom"), help_text=_("C'est sous ce nom qu'apparaîtra l'école"))
    short_name = models.CharField(max_length=20, verbose_name=_("Abréviation (ou pseudo)"), null=True, blank=True)
    email = models.EmailField(max_length=100, verbose_name=_("Email"),
        help_text=_("Apparaîtra sur les documents. Nous l'utiliserons pour contacter l'école"))
    phone_number = models.CharField(max_length=255, verbose_name=_("Nº de téléphone"),
        help_text=_("Apparaîtra sur les documents. Nous l'utiliserons pour contacter l'école"))
    country = CountryField(max_length=255, verbose_name=_("Pays"), null=True, help_text=_("Le pays du siège de l'école"))
    zip_code = models.CharField(max_length=255, verbose_name=_("Code postal"), null=True, blank=True)
    region = models.CharField(max_length=255, verbose_name=_("Région"), null=True, blank=True)
    city = models.CharField(max_length=255, verbose_name=_("Ville/Localité"), null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name=_("Adresse"), null=True, blank=True)
    website = models.URLField(null=True, blank=True, verbose_name=_("Site web"))
    logo = models.ImageField(upload_to="companies/logos/%Y/", null=True, blank=True, verbose_name=_("Logo"))
    details = models.TextField(null=True, blank=True, verbose_name=_("Plus de détails"))
    on_trial = models.BooleanField(default=True, verbose_name=_("Période d'essai"))
    is_active = models.BooleanField(default=False, verbose_name=_("Actif"),
        help_text=_("Désigne si la compagnie est active ou pas. Si elle est incative, le compte sera inacessible"))
    is_primary_tenant = models.BooleanField(default=False, verbose_name=_("Schéma public (à cause de la base de données)"), null=True, blank=True,
        help_text=_("Désigne si l'objet est le schéma (DB) public. Doit être unique. À ne pas toucher"), editable=False)
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="UUID", editable=False)
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))
    updated_on = models.DateTimeField(auto_now=True, verbose_name=_("Date de modification"))
    extra_data = models.JSONField(null=True, blank=True, verbose_name=_("Données supplémentaires"))
    
    # School owner
    owner_first_name = models.CharField(max_length=200, verbose_name=_("Prénom(s) du proprio"), null=True, blank=True)
    owner_last_name = models.CharField(max_length=200, verbose_name=_("Nom de famille du proprio"), null=True, blank=True)
    owner_phone_number = models.CharField(max_length=25, verbose_name=_("Nº de téléphone du proprio"), null=True, blank=True)
    owner_email = models.EmailField(verbose_name=_("Email du proprio"), null=True, blank=True)

    # code to distinguish teacher and student
    # to be send to the Pricipal on school creation so as to create teachers and student
    teacher_code = models.CharField(max_length=255, verbose_name=_("Code prof"), null=True, blank=True)
    student_code = models.CharField(max_length=255, verbose_name=_("Code eleve"), null=True, blank=True)
    
    auto_create_schema = True # default true, schema will be automatically created and synced when it is saved
    
    class Meta:
        verbose_name = _("École")
        verbose_name_plural = _("Écoles")
        ordering = ["name", "country", "on_trial", "is_active", "date"]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.badge:
            self.badge = self.generate_badge()
        self.teacher_code = self.badge + "-TEACHER"
        self.student_code = self.badge + "-STUDENT"
        super(School, self).save(*args, **kwargs)
    
    
    @property
    def business_name(self):
        return self.name
    
    
    @property
    def code(self):
        return self.badge
    
    @property
    def primary_domain(self):
        return self.get_primary_domain()
    
    @property
    def meta_settings(self):
        try:
            _meta_settings = self.meta_settings_model # from SchoolMetaSettings() model
        except SchoolMetaSettings.DoesNotExist:
            _meta_settings = SchoolMetaSettings.objects.create(company=self)
        except:
            _meta_settings = None
        return _meta_settings
    
    
    @property
    def get_primary_domain_full_url(self) -> str:
        """ 
        Full primary URL (domain name) of the current school.
        
        Returns:
            (e.g.: https://demo.domain.com/ or https://domain.com/r/demo/)
        """
        tenant_domain = self.get_primary_domain().domain # or tenant_subfolder
        
        # tenant domain mechanism: {subdomain}.domain.com/ (subdomain mechanism)
        if settings.PRODUCTION_MODE: # on production
            return tenant_domain
        
        # dev mode
        return f"http://{tenant_domain}:8000/" # if you launch the server with a different port, this will fail
    
    
    
    def generate_badge(self):
        """ Generate a unique ID (badge for a given school) """
        return "".join(random.choices(string.ascii_uppercase + string.digits, k=10)) # you can change the length




class Domain(DomainMixin):
    is_primary_tenant_domain = models.BooleanField(default=False, verbose_name=_("Domaine du schéma public"),
        help_text=_("Désigne si le domaine appartient au site officiel (Only primary tenant domains can have this attribute)"),
        editable=False, null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name=_("Actif"))
    details = models.TextField(null=True, blank=True, verbose_name=_("Plus de détails"))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))
    updated_on = models.DateTimeField(auto_now=True, verbose_name=_("Date de modification"))
    extra_data = models.JSONField(null=True, blank=True, verbose_name=_("Données supplémentaires"))
    
    class Meta:
        verbose_name = _("Nom de domaine")
        verbose_name_plural = _("Noms de domaines")
        unique_together = [("is_primary", "tenant")]
        ordering = ["is_active", "date"]
    
    def __str__(self):
        return f"{self.domain} :: {self.tenant}"
    
    def save(self, *args, **kwargs):
        # If self.is_primary_tenant_domain is True, domain tenant must be the public/base tenant
        if self.is_primary_tenant_domain:
            # get public tenant
            try:
                public_schema_tenant = School.objects.get(schema_name=str(settings.PUBLIC_SCHEMA_NAME or "public")) # by default, it's "public"
                # if tenant exists but is not primary, self.is_primary_tenant_domain must be set to False
                if public_schema_tenant.is_primary_tenant:
                    self.is_primary_tenant_domain = True
                else:
                    self.is_primary_tenant_domain = False
            except:
                # If tenant doesn't exist or any other exception then self.is_primary_tenant_domain must be set to False
                self.is_primary_tenant_domain = False
                pass
        
        super(Domain, self).save(*args, **kwargs)





class SchoolMetaSettings(models.Model):
    """ Model to consider while configuring a school. Fields are considered as attributes """
    
    school = models.OneToOneField(School, on_delete=models.CASCADE, verbose_name=_("École`"), related_name="meta_settings_model")
    display_logo = models.BooleanField(default=True, verbose_name=_("Votre logo peut être affiché au public"),
        help_text=_("Désigne si le logo de votre école (si vous en avez) peut être affiché au grand public"))
    display_name = models.BooleanField(default=True, verbose_name=_("Votre nom peut être affiché au public"),
        help_text=_("Désigne si le nom de votre école peut être affiché au grand public"))
    details = models.TextField(null=True, blank=True, verbose_name=_("Plus de détails"))
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="UUID", editable=False, unique=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))
    updated_on = models.DateTimeField(auto_now=True, verbose_name=_("Date de modification"))
    extra_data = models.JSONField(null=True, blank=True, verbose_name=_("Données supplémentaires"))
    
    class Meta:
        verbose_name = _("Paramètre pour école")
        verbose_name_plural = _("Paramètres des écoles")
        ordering = ["-date", "school"]
    
    def __str__(self):
        return f"Paramètres de {self.school.name} ({self.school.badge})"
