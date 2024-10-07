"""
sending confoirmation email
"""
from accounts.models import User
from django.db.models.signals import post_save
from school_management.services.email_services import SendRawEmailService
from utilities.utils import generate_activation_link

def send_signal(sender, instance, created,  **kwargs):
    email_content = f"please confirm your account using this link {generate_activation_link(user=instance)}"
    if created:
        email = SendRawEmailService(request=None, mail_subject="Dreametrix email confirmation", email_content=email_content, context={}, receivers=[str(instance.email)])
        email.send_email_by_default()
        print("email sent")



post_save.connect(send_signal, sender=User)