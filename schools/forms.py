from django import forms
from schools.models import School
from django_summernote.widgets import SummernoteWidget


class CreateSchoolForm(forms.ModelForm):
    """
    School creation form.
    Using a ModelForm because I don't want to define form fields manually.
    """
    
    class Meta:
        model = School
        fields = ["name", "slogan", "short_name", "email", "phone_number", "country", "zip_code", "region", "city", "address",
            "website", "details", "owner_first_name", "owner_last_name", "owner_phone_number", "owner_email"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "slogan": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "short_name": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "email": forms.EmailInput(attrs={"class": "form-control form-control-sm"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "country": forms.Select(attrs={"class": "form-select form-select-sm select2"}),
            "zip_code": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "region": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "city": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "address": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "website": forms.URLInput(attrs={"class": "form-control form-control-sm"}),
            "details": SummernoteWidget(attrs={"class": "form-control form-control-sm"}),
            "owner_first_name": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "owner_last_name": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "owner_phone_number": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "owner_email": forms.EmailInput(attrs={"class": "form-control form-control-sm"}),
        }
    
    
    def save(self, *args, **kwargs):
        """
        Overriding the default save method so that, it's not possible to save school directly with the current form.
        Is designed to save data in session and proceed creation using a task utility (see schools.tasks or schools.after_response).
        """
        return
