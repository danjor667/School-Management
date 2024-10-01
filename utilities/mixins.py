import json

from django.db import models
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _


class GenderMixin(models.Model):
    class GenderChoices(models.TextChoices):
        MALE = ("male", _("Masculin"))
        FEMALE = ("female", _("Féminin"))
        OTHERS = ("others", _("Divers"))
        UNDEFINED = ("undefined", _("Non défini"))
    
    gender = models.CharField(choices=GenderChoices.choices, max_length=10, verbose_name=_("Genre"), default=GenderChoices.UNDEFINED,
        null=True, blank=True, help_text=_("Vous pouvez préciser le genre s'il s'agit d'une personne"))
    
    class Meta:
        abstract = True
    
    @property
    def gender_is_male(self) -> bool:
        return self.gender == GenderMixin.GenderChoices.MALE
    
    @property
    def gender_is_female(self) -> bool:
        return self.gender == GenderMixin.GenderChoices.FEMALE
    
    @property
    def gender_is_others(self) -> bool:
        return self.gender == GenderMixin.GenderChoices.OTHERS
    
    @property
    def gender_is_undefined(self) -> bool:
        return self.gender == GenderMixin.GenderChoices.UNDEFINED




class PersonModelMixin(GenderMixin):
    """
    PersonModelMixin provides an easy way to share person's fields, attributes and properties across models.
    Means that you no more need to define fields like lastname, firstname, … They are defined already in this mixin.
    
    Args:
        GenderMixin (ModelMixin): Mixin that contains gender's field, properties and attributes
    """
    first_name = models.CharField(max_length=255, verbose_name=_("Prénom"), null=True)
    last_name = models.CharField(max_length=255, verbose_name=_("Nom"), null=True)
    email = models.EmailField(max_length=100, verbose_name=_("Adresse électronique"), null=True, blank=True)
    phone_number = models.CharField(max_length=255, verbose_name=_("Nº de téléphone"), null=True, blank=True)
    country = CountryField(verbose_name=_("Pays"), null=True, blank=True)
    zip_code = models.CharField(max_length=50, verbose_name=_("Code postal"), null=True, blank=True)
    city = models.CharField(max_length=50, verbose_name=_("Ville"), null=True, blank=True)
    address = models.CharField(max_length=100, verbose_name=_("Adresse"), null=True, blank=True)
    age = models.IntegerField(null=True, blank=True, verbose_name=_("Âge"))
    picture = models.ImageField(upload_to="accounts/avatars/%Y/", null=True, blank=True, verbose_name=_("Photo"))
    bio = models.TextField(max_length=500, verbose_name=_("Biographie"), null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_("Date de création"), null=True)
    updated_on = models.DateTimeField(auto_now=True, verbose_name=_("Dernières modifications"))
    extra_data = models.JSONField(null=True, blank=True, verbose_name=_("Données supplémentaires"))
    
    class Meta:
        abstract = True
    
    @property
    def date(self):
        return self.created_on
    
    @property
    def date_joined(self):
        return self.created_on
    
    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return "{} {}".format(self.first_name, self.last_name)
        elif self.first_name:
            return "{}".format(self.first_name)
        elif self.last_name:
            return "{}".format(self.last_name)
        return self.pk
    
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
    def full_address(self):
        return self.get_full_address
    
    
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
