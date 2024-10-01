import ssl
from typing import List
from django.conf import settings
from accounts.models import User
from django.http import HttpRequest
from django.utils.functional import cached_property
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.core.mail import EmailMessage, get_connection
from django.core.mail.backends.smtp import EmailBackend as SMTPBackend


class DevEmailBackend(SMTPBackend):
    """
    Email backend to use (only) in dev mode (it doesn't check hostname while creating connection).
    While being in dev mode Django doesn't allow email sending directly to email address (only console backend works).
    To override this and to be able to send actual email in dev mode, use this as email backend.

    Args:
        SMTPBackend (_type_): A wrapper that manages the SMTP network connection.

    Returns:
        SSLContext: SSLContext instance
    """
    @cached_property
    def ssl_context(self):
        if self.ssl_certfile or self.ssl_keyfile:
            ssl_context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)
            ssl_context.load_cert_chain(self.ssl_certfile, self.ssl_keyfile)
            return ssl_context
        else:
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            return ssl_context





class SendEmailWithTemplateService:
    """
    Send email to users using templates (instead of plain HTML codes)
    """
    
    def __init__(self, request: HttpRequest|None, mail_subject: str, mail_template: str, context: dict, receivers: List[str]) -> None:
        self.request = request
        self.mail_subject = mail_subject
        self.mail_template = mail_template
        self.context = context
        self.receivers = receivers
        
        self.email_content = render_to_string(self.mail_template, self.context)
        self.context.update({"mail_subject": self.mail_subject,})
    
    
    def _custom_connection(self, from_email_address: str, password: str):
        """ Send email with custom connection (not using default email)
        
        Args:
            from_email_address (str): Email address to use for this custom connection
            password (str): Password of the email address to use for this custom connection
        
        Returns:
            _type_: _description_
        """
        return get_connection(
            backend=settings.EMAIL_BACKEND,
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=from_email_address,
            password=password,
            use_tls=settings.EMAIL_USE_TLS
        )
    
    
    def send_email_by_default(self):
        email = EmailMessage(
            subject=self.mail_subject,
            body=self.email_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=self.receivers
        )
        email.content_subtype = "html"
        email.send()
        return _("Email envoyé avec succès !")
    
    
    def user_send_no_reply_email(self, sender: User):
        """ Send (no reply) email by including user's full name in sender address """
        
        with self._custom_connection(from_email_address=settings.EMAIL_HOST_USER, password=settings.EMAIL_HOST_PASSWORD) as connection:
            _from_email_str = str(_(f"{sender.full_name} via {settings.SITE_NAME} <{settings.EMAIL_HOST_USER}>"))
            email = EmailMessage(
                subject=self.mail_subject,
                body=self.email_content,
                from_email=_from_email_str,
                to=self.receivers,
                connection=connection,
            )
            email.content_subtype = "html"
            email.send()
            return _(f"Email (via {_from_email_str}) envoyé avec succès !")




class SendRawEmailService:
    """
    Send email to users whithout templates (using plain text/HTML)
    """
    
    def __init__(self, request: HttpRequest|None, mail_subject: str, email_content: str, context: dict, receivers: List[str]) -> None:
        self.request = request
        self.mail_subject = mail_subject
        self.email_content = email_content
        self.context = context
        self.receivers = receivers
        
        self.context.update({"mail_subject": self.mail_subject,})
    
    
    def send_email_by_default(self):
        email = EmailMessage(
            subject=self.mail_subject,
            body=self.email_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=self.receivers
        )
        email.content_subtype = "html"
        email.send()
        return _("Email envoyé avec succès !")
