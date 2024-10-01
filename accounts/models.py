import uuid, json
from django.db import models
from utilities.mixins import GenderMixin
from accounts.managers import UserManager
from django_countries.fields import CountryField
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser, GenderMixin):
    """ Main User model
    
    Args:
        AbstractUser: base AbstractUser from django
        GenderMixin: Mixin to use in models that require a "gender" field. Comes with its own methods and properties
    """
    email = models.EmailField(max_length=100, unique=True, verbose_name=_("Adresse électronique"))
    phone_number = models.CharField(max_length=255, verbose_name=_("Nº de téléphone"), null=True, blank=True)
    country = CountryField(verbose_name=_("Pays"), null=True, blank=True)
    zip_code = models.CharField(max_length=50, verbose_name=_("Code postal"), null=True, blank=True)
    city = models.CharField(max_length=50, verbose_name=_("Ville"), null=True, blank=True)
    address = models.CharField(max_length=100, verbose_name=_("Adresse"), null=True, blank=True)
    age = models.IntegerField(null=True, blank=True, verbose_name=_("Âge"))
    picture = models.ImageField(upload_to="accounts/avatars/%Y/", null=True, blank=True, verbose_name=_("Photo de profil"))
    bio = models.TextField(max_length=500, verbose_name=_("Biographie"), null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="UUID", unique=True, editable=False)
    is_dev = models.BooleanField(default=False, verbose_name=_("Développeur"), help_text=_("Utilisateur développeur"), editable=False)
    temporary_password = models.CharField(max_length=500, null=True, blank=True, verbose_name=_("Mot de passe temporaire"), editable=False)
    updated_on = models.DateTimeField(auto_now=True, verbose_name=_("Date de modification"))
    extra_data = models.JSONField(null=True, blank=True, verbose_name=_("Données supplémentaires"))
    
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    class Meta:
        verbose_name = _("Utilisateur")
        verbose_name_plural = _("Utilisateurs")
        ordering = ["-date_joined", "email", "first_name", "last_name", "gender", "age", "username", "country"]
    
    def __str__(self):
        return f"{self.email} : {self.full_name}"
    
    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return "{} {}".format(self.first_name, self.last_name)
        elif self.first_name:
            return "{}".format(self.first_name)
        elif self.last_name:
            return "{}".format(self.last_name)
        return self.username
    
    @property
    def get_full_name(self):
        return self.full_name
    
    @property
    def get_full_address(self):
        full_address = None
        if self.address:
            full_address = self.address
        if self.address and self.city:
            full_address = f"{self.address}, {self.city}"
        if self.address and self.city and self.zip_code:
            full_address = f"{self.address}, {self.city} {self.zip_code}"
        if self.address and self.city and self.zip_code and self.country:
            full_address = f"{self.address}, {self.city} {self.zip_code}, {self.country.name}"
        return full_address
    
    
    @property
    def temp_pass(self):
        return self.temporary_password
    
    @property
    def has_temporary_password(self):
        """ Check if current user has a temporary password (then we could invite him/her to update it) """
        if self.temporary_password and self.temporary_password is not None:
            return True
        return False
    
    def set_temporary_password(self, raw_password: str):
        """
        Save current user temporary password. Same algo as self.set_password(...) but with saving user's raw password in a field
        """
        self.temporary_password = str(raw_password)
        self.save()
        self.set_password(raw_password=self.temporary_password)
        return self
    
    
    @property
    def cleaned_extra_data_to_dict(self):
        """
        Clean extra data (from field `extra_data`) of the current user and return it.
        If `self.extra_data` is not a dict or can't be converted to a dict, return None
        
        Returns:
            dict: Cleaned extra data of current user/manager obj
        """
        
        if isinstance(self.extra_data, dict):
            return self.extra_data
        
        # else
        try:
            extra_data = json.dumps(self.extra_data) # By default type(self.extra_data) == str
            extra_data = dict(self.extra_data)
            return extra_data
        except:
            # do what you want here
            return None
