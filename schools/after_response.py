import random, string, logging

# django
from django.conf import settings
from django.http import HttpRequest
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

# utils
import after_response
from django_tenants.utils import tenant_context
from school_management.services.email_services import SendRawEmailService
from utilities.utils import format_tenant_schema_name, format_tenant_domain_name

# models
from accounts.models import User
from schools.models import School, Domain


# logs setup
logging.basicConfig(level=logging.ERROR)



def _generate_unique_str(length=6):
    """ Generate a unique string to append to schema name if schema name already exists. """
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length)).lower()



def _proceed_school_creation(request: HttpRequest|None, data: dict, submited_by) -> School:
    """
    A utility (background) to save school data
    
    Args:
        request (HttpRequest | None): WSGI/ASGI HTTP Request or None
        data (dict): A dictionnary that comes from session (see serializer/form)
        submited_by (User | None): User or admin who submited this creation request
    
    Returns:
        school (School): Created school (tenant object)
    """
    
    _schema = format_tenant_schema_name(slugify(data.get("name")))
    school = School()
    
    # getting schema name
    school.schema_name = _schema
    if School.objects.filter(schema_name=_schema).exists(): # check if schema already exists, then change it
        school.schema_name = f"{_schema}_{_generate_unique_str()}" # school obj doesn't exist for now, so has no pk
    
    # let's proceed other fields
    school.created_by = submited_by
    school.name = data.get("name")
    school.email = data.get("email")
    school.phone_number = data.get("phone_number")
    school.slogan = data.get("slogan")
    school.short_name = data.get("short_name")
    school.country = data.get("country")
    school.zip_code = data.get("zip_code")
    school.region = data.get("region")
    school.city = data.get("city")
    school.address = data.get("address")
    
    school.website = data.get("website")
    school.details = data.get("details")
    school.owner_first_name = data.get("owner_first_name")
    school.owner_last_name = data.get("owner_last_name")
    school.owner_phone_number = data.get("owner_phone_number")
    school.owner_email = data.get("owner_email")
    
    # custom details
    school.on_trial = True
    school.is_active = False
    school.is_primary_tenant = False # see model's field for more details about this particular field
    
    # saving data
    school.save()
    
    # do what you want with the "request" arg here
    
    return school




def _proceed_school_domain_name(request: HttpRequest, school: School) -> Domain:
    """
    """
    domain_details = _(f"""
        Nom de domain de l'école '{school.name}' immatriculé au #{school.badge}.
    """)
    
    _domain_name = format_tenant_domain_name(slugify(school.name))
    domain = Domain()
    
    # getting domain name
    domain.domain = _domain_name
    if Domain.objects.filter(domain=_domain_name).exists(): # check if domain name (subdomain) already exists, then change it
        # append only three chars. Pay attention to the DASH (-) instead of an underscore (_)
        domain.domain = f"{_domain_name}-{_generate_unique_str(length=3)}"
    
    # check if school already has a primary domain name (because it's supposed to be unique)
    domain.is_primary = True
    if Domain.objects.filter(is_primary=True, tenant=school).exists(): # then this new domain shouldn't be the primary one
        domain.is_primary = False
    
    # let's proceed other fields
    domain.tenant = school
    domain.is_active = False # should be activated later on
    domain.is_primary_tenant_domain = False # see model's field for more details about this particular field
    domain.details = domain_details
    
    # saving data
    domain.save()
    
    # do what you want with the "request" arg here
    
    return domain




def _creation_processes_completed(request: HttpRequest, submited_by, school: School, domain: Domain) -> None:
    """
    After other stuffs have been completed, notify the admin who submited the request.
    
    Args:
        request (HttpRequest): WSGI/ASGI HTTP Request
        submited_by (User): The admin that submited this creation request
        school (School): Created school
        domain (Domain): Created domain
    """
    
    # switch to school schema
    with tenant_context(school):
        # notify school's owner here if you want
        
        try:
            mail_subject = _(f"La requête de création de l'école # {school.name} # que vous avez soumise")
            email_content = _(f"""
                Bonjour {submited_by.full_name}, \n
                Par la présente, nous vous informons que le processus de création de l'école # {school.name} #
                que vous avez initié est maintenant terminé. Vous pouvez consulter les détails via le dashboard ! \n \n \n
                Cordialement, \n
                L'équipe {settings.SITE_NAME} !
            """)
            email_context = {
                "school": school,
                "domain": domain,
                "request": request,
                "submited_by": submited_by,
                "mail_subject": mail_subject,
                "settings": settings,
            }
            
            email = SendRawEmailService(
                request=request,
                mail_subject=mail_subject,
                email_content=email_content,
                context=email_context,
                receivers=[submited_by.email]
            )
            email.send_email_by_default()
        except Exception as e:
            logging.error(f"Email sending failed. Error: {e}")





@after_response.enable
def create_school_schema_and_domain_task(request: HttpRequest|None, data: dict, submited_by):
    """
    Task to create a school (with its base details and domain).
    
    Args:
        request (HttpRequest | None): WSGI/ASGI HTTP Request or None
        data (dict): A dictionnary that comes from session (see serializer/form)
        submited_by (User | None): User or admin who submited this creation request
    
    Returns:
        None
    """
    # school
    school = _proceed_school_creation(
        request=request,
        data=data,
        submited_by=submited_by
    )

    student_code = f"{school.badge}-STUDENT"
    teacher_code = f"{school.badge}-TEACHER"
    email_content = f"Here is the student code: {student_code} and teacher code: {teacher_code} for {school.name}"
    email = SendRawEmailService(request, mail_subject="SignUp Codes", email_content=email_content, context={},
                                receivers=[submited_by.email])
    email.send_email_by_default()
    
    # domain name (subdomain)
    domain = _proceed_school_domain_name(request=request, school=school)
    
    # all processes completed, send notifications
    processes = _creation_processes_completed(
        request=request,
        submited_by=submited_by,
        school=school,
        domain=domain
    )
