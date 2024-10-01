from django.conf import settings
from schools.models import School, Domain
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Create base database schemas and domains for the following project"
    
    
    def handle(self, *args, **options):
        self.stdout.write("Creating database base schema (public)")
        
        try:
            self.create_public_schema_and_domain()
            self.stdout.write(self.style.SUCCESS(">> Database public schema created successfully -> OK \n\n"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Database public schema creation failed: {str(e)} \n\n"))
    
    
    def create_public_schema_and_domain(self):
        tenant = self.create_public_schema()
        domain = self.create_public_domain(tenant=tenant)
        return tenant, domain
    
    
    def create_public_schema(self):
        # Creating schema
        tenant = School()
        tenant.schema_name = "public"
        tenant.name = str(settings.SITE_NAME)
        tenant.email = "public@example.com"
        tenant.phone_number = "000000000000"
        tenant.zip_code = "000000000000"
        tenant.region = "000000000000"
        tenant.city = "000000000000"
        tenant.address = "000000000000"
        tenant.website = str(settings.BASE_DOMAIN_NAME)
        tenant.details = "000000000000"
        tenant.logo = None
        tenant.country = None
        tenant.is_active = True
        tenant.is_primary_tenant = True
        tenant.on_trial = False
        tenant.owner_first_name = "000000000000"
        tenant.owner_last_name = "000000000000"
        tenant.owner_phone_number = "000000000000"
        tenant.owner_email = "public@example.com"
        tenant.save()
        return tenant
    
    
    def create_public_domain(self, tenant: School):
        # Add one or more domains for the tenant
        domain = Domain()
        domain.domain = str(settings.BASE_DOMAIN_NAME)
        domain.tenant = tenant
        domain.is_primary = True
        domain.is_active = True
        domain.is_primary_tenant_domain = True
        domain.details = "000000000000"
        domain.save()
        return domain
