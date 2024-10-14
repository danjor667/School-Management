import logging, re
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpRequest
from django.shortcuts import redirect
from django.utils.text import slugify
from hitcount.views import HitCountMixin
from hitcount.utils import get_hitcount_model
from django.utils.crypto import get_random_string


# configure logging
logging.basicConfig(level=logging.ERROR)


def get_client_ip_address(request: HttpRequest) -> str:
    """ Get client IP address """
    try:
        ip_address = request.META.get("HTTP_X_REAL_IP")
    except:
        ip_address = request.META.get("REMOTE_ADDR")
    
    if not ip_address or ip_address is None:
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(",")[0]
        else:
            ip_address = request.META.get("REMOTE_ADDR")
    
    return str(ip_address)




def generate_otp_code(code_len: int) -> str:
    """Generate a random number of n digits
    
    Args:
        code_len (int): Length of code to be generated (we can use settings.OTP_CODE_LENGTH)
    
    Returns:
        str: Generated code in string format.
    """
    return get_random_string(length=code_len, allowed_chars="0123456789")




def _format_tenant_schema_and_domain(_str: str, repl: str):
    """ A (private) function to format tenant domain name and schema name
    
    Args:
        _str (str): String to format (e.g. School's name)
        repl (str): Character for replacing not allowed chars (or spaces)
    """
    VALID_REPL_CHARS = {"-", "_"} # Allow only - (dash) and _ (underscore)
    
    if _str is None or _str == "" or _str == " ": # None, empty or white space
        raise ValueError("Incorrect value of _str arg")
    elif repl not in VALID_REPL_CHARS:
        raise ValueError("Replacing character must be one of %r." % VALID_REPL_CHARS)
    
    # Everything is ok, then continue
    
    # Replacing all non-english alphabet chars by spaces (e.g. démo9 schema@ -> d mo schema)
    with_space_formated = re.sub(r"[^a-zA-Z]", " ", _str)
    
    # Replacing all spaces by repl value
    with_repl_formated = re.sub(r"\s+", repl, with_space_formated).lower()
    return with_repl_formated




def format_tenant_schema_name(_str: str) -> str:
    """ Format a new tenant schema name (with underscores (_))
    
    Args:
        name (str): School name or any other string
    
    Returns:
        (str): Formated schema_name
    """
    return _format_tenant_schema_and_domain(_str=_str, repl="_")



def format_tenant_domain_name(_str: str) -> str:
    """ Generate a tenant full domain name (subdomain) based on its schema
    
    Args:
        schema_name (str): Tenant schema name or any other string
    
    Returns:
        (str): Formated full domain name (i.e. demo) (using subfolder structure, demo.sample.com -> sample.com/r/demo)
    """
    with_dash_formated = _format_tenant_schema_and_domain(_str=_str, repl="-")
    full_format = with_dash_formated.replace("_", "-") # replacing underscores with dashes
    
    full_domain_name = f"{full_format}.{str(settings.BASE_DOMAIN_NAME)}".lower() # i.e demo.example.com or demo.localhost
    
    return full_domain_name





def update_views(request: HttpRequest, object):
    """ Hit count on objects """
    try:
        context = {}
        hit_count = get_hitcount_model().objects.get_for_object(object)
        hits = hit_count.hits
        hitcontext = context["hitcount"] = {"pk": hit_count.pk}
        hit_count_response = HitCountMixin.hit_count(request, hit_count)

        if hit_count_response.hit_counted:
            hits = hits + 1
            hitcontext["hitcounted"] = hit_count_response.hit_counted
            hitcontext["hit_message"] = hit_count_response.hit_message
            hitcontext["total_hits"] = hits
    
    except Exception as e:
        logging.warn(f"Unable to create hitcount obj : {str(e)}")


def redirect_to_tenant_domain(user):
    protocol = "http"
    tenant_domain = format_tenant_domain_name(user.tenant.schema_name)
    return redirect(f"{protocol}://{tenant_domain}:8000")


def generate_activation_link(user):
    token = default_token_generator.make_token(user)
    # base_url = reverse("schools:activate-user")
    base_url = "activate-user"
    if settings.PRODUCTION_MODE:
        full_url = f"https://school-management-uoil.onrender.com/{base_url}?token={token}$user_id={user.id}"
    else:
        full_url = f"http://localhost:8000/{base_url}/?token={token}&user_id={user.id}"
    return full_url