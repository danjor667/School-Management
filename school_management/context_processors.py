from django.conf import settings
from django.utils.translation import get_language


def global_context(request):
    context = {
        "settings": settings,
        "current_language_code": get_language(),
    }
    return context




def tenant_context(request):
    try:
        tenant = request.tenant
    except:
        tenant = None
    
    context = {
        "tenant": tenant,
        "company": tenant,
        "school": tenant,
    }
    return context
