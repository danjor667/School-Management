from accounts.signals import send_signal
from django.db.models.signals import post_save

from tenant_users.models import TenantUser

post_save.connect(send_signal, sender=TenantUser)