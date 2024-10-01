from schools.models import School
from rest_framework import serializers


class SchoolSerializer(serializers.ModelSerializer):
    """
    Serializer class to create a new school.
    Using a ModelSerializer because I don't want to define fields manually.
    """
    
    class Meta:
        model = School
        fields = ["name", "slogan", "short_name", "email", "phone_number", "country", "zip_code", "region", "city", "address",
            "website", "logo", "details", "owner_first_name", "owner_last_name", "owner_phone_number", "owner_email"]
    
    
    def save(self, *args, **kwargs):
        """
        Overriding the default save method so that, it's not possible to save school directly with the current serializer.
        Is designed to save data in session and proceed creation using a task utility (see schools.tasks or schools.after_response).
        """
        return
