
"""
    Generated by "django-admin startproject" using Django 5.0.4 and then customized.
"""
from pathlib import Path
from decouple import config
from django.utils.translation import gettext_lazy as _


#############################################################
#############################################################
#############################################################
#######                                             #########
#######                                             #########
#######                  ROOT CONFIGS               #########
#######                                             #########
#######                                             #########
#############################################################
#############################################################
#############################################################

# this is the first ever (and only unique) conf to change if you want to switch from dev mode to production
PRODUCTION_MODE = True # if set to True, all production's configs will be activated by default
PRODUCTION_MAIN_DOMAIN_NAME = "" # main domain name to use on production (without protocol or port). Should be updated

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config("SECRET_KEY")

DEBUG = False

# if PRODUCTION_MODE:
#     DEBUG = False

APPEND_SLASH = True


ALLOWED_HOSTS = ["*"]
INTERNAL_IPS = ["127.0.0.1"]
SITE_ID = 1
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
ROOT_URLCONF = "school_management.urls.tenants_urls" #  separate tenant's URLs from public URLs. It was "school_management.urls"
WSGI_APPLICATION = "school_management.wsgi.application"


ADMINS = [
    ("Jordan Nguepi", "jordannguepi@gmail.com")
    # put your own infos here
]


SITE_NAME = "School SAAS" #  Custom conf to use if needed. Defines website official's name




#############################################################
#############################################################
#############################################################
#######                                             #########
#######                                             #########
#######       INSTALLED APPLICATIONS DEFINITION     #########
#######                                             #########
#######                                             #########
#############################################################
#############################################################
#############################################################
SHARED_APPS = [
    # following apps should stay at top of apps definition
    "django_tenants", # Django tenants 
    "schools.apps.SchoolsConfig", # app tenant model resides in
    
    
    "django.contrib.contenttypes", # required by "django-tenants"
    
    # django core apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize", # Added
    "django.contrib.sitemaps", # Added
    "django.contrib.postgres", # Added
    "django.contrib.sites", # Added
    "django.contrib.admindocs", # Docuementation of models fields in admin page
    
    
    # 3rd PARTY APPS
    "storages",
    "django_htmx",
    "crispy_forms", # styling forms to filter querysets
    "django_filters",
    "after_response",
    "django_countries",
    "django_summernote",
    "django_extensions",
    "django_ckeditor_5",
    "django_celery_beat",
    "crispy_bootstrap4", # template pack of crispy_forms
    "django_celery_results",
    
    
    # LOCALE SHARED APPS
    "academic_years.apps.AcademicYearsConfig", # Years App (shared by all schools)
    "accounts.apps.AccountsConfig",
    "utilities.apps.UtilitiesConfig",
]

# Apps that are loaded only in dev mode
if DEBUG:
    SHARED_APPS += [
        "django_browser_reload", # Relaod automatically browser after changes
    ]


# tenant's apps (may be ordered alphabetically, just to avoid duplicated apps)
TENANT_APPS = [
    "hitcount",
    #"easyaudit",
    "import_export",
    "notifications",
    
    "classes.apps.ClassesConfig",
    "dashboard.apps.DashboardConfig",
    "grades.apps.GradesConfig",
    "home_works.apps.HomeWorksConfig",
    "parents.apps.ParentsConfig",
    "quizzes.apps.QuizzesConfig",
    "staffs.apps.StaffsConfig",
    "students.apps.StudentsConfig",
    "teachers.apps.TeachersConfig",
    "tenant_users.apps.TenantUsersConfig",
]

# apps definition
INSTALLED_APPS = SHARED_APPS + [app for app in TENANT_APPS if app not in SHARED_APPS]







#############################################################
#############################################################
#############################################################
#######                                             #########
#######                                             #########
#######             MIDDLEWARES                     #########
#######                                             #########
#######                                             #########
#############################################################
#############################################################
#############################################################
MIDDLEWARE = [
    "django_tenants.middleware.main.TenantMainMiddleware", # Django tenants (TenantSubfolderMiddleware | TenantMainMiddleware)
    
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Serving static files
    "django.contrib.sessions.middleware.SessionMiddleware",
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.admindocs.middleware.XViewMiddleware", # Docuementation of models fields in admin page
    
    "django_htmx.middleware.HtmxMiddleware",  # Django HTMX
    "htmlmin.middleware.HtmlMinifyMiddleware", # HTML minifier
    "htmlmin.middleware.MarkRequestMiddleware", # HTML minifier
    
    "easyaudit.middleware.easyaudit.EasyAuditMiddleware", # Easy Audit
]


# API based MIDDLEWARES
MIDDLEWARE += [
    "corsheaders.middleware.CorsMiddleware", # Corsheaders
]


# middlewares that are loaded only in dev mode
if DEBUG:
    MIDDLEWARE += [
        "django_browser_reload.middleware.BrowserReloadMiddleware", # Django Browser Reload
    ]


######################################################
######################################################
######################################################
########                                       #######
#######       Backend config                     #####
#######                                     ##########
#######################################################
#####################################################

AUTHENTICATION_BACKENDS = [
    "school_management.backend.DefaultBackend",
    "school_management.backend.TenantBackend",
]








#############################################################
#############################################################
#############################################################
#######                                             #########
#######                                             #########
#######                 TEMPLATES                   #########
#######                                             #########
#######                                             #########
#############################################################
#############################################################
#############################################################
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                
                # Custom context processors
                "school_management.context_processors.global_context",
                "school_management.context_processors.tenant_context",
            ],
        },
    },
]








#############################################################
#############################################################
#############################################################
#######                                             #########
#######                                             #########
#######               DATABASES                     #########
#######                                             #########
#######                                             #########
#############################################################
#############################################################
#############################################################
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

# Development databases
DATABASES = {
    "default": {
        "ENGINE": config("DB_ENGINE"),
        "PASSWORD": config("DB_PASSWORD"),
        "NAME": config("DB_NAME"),
        "HOST": config("DB_HOST"),
        "USER": config("DB_USER"),
        "PORT": config("DB_PORT"),
    }
}


DATABASE_ROUTERS = [
    "django_tenants.routers.TenantSyncRouter",
]

AUTH_USER_MODEL = "accounts.User"











#############################################################
#############################################################
#############################################################
#######                                             #########
#######                                             #########
#######             PASSWORD VALIDATORS             #########
#######                                             #########
#######                                             #########
#############################################################
#############################################################
#############################################################
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]









#############################################################
#############################################################
#############################################################
#######                                             #########
#######                                             #########
#######             INTERNATIONALIZATION            #########
#######                                             #########
#######                                             #########
#############################################################
#############################################################
#############################################################
LANGUAGE_CODE = "fr"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True







#############################################################
#############################################################
#############################################################
#######                                             #########
#######                                             #########
#######          STATIC & MEDIA FILES CONFIGS       #########
#######                                             #########
#######                                             #########
#############################################################
#############################################################
#############################################################
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "collectstatic/"

MEDIA_URL = "uploads/"
MEDIA_ROOT = BASE_DIR / "mediafiles/uploads"

STATICFILES_DIRS = [BASE_DIR / "static/"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"





#############################################################
#############################################################
#############################################################
#######                                             #########
#######                                             #########
#######                  EMAIL CONFIGS              #########
#######                                             #########
#######                                             #########
#############################################################
#############################################################
#############################################################
# Dev mode EMAIL_BACKEND
#EMAIL_BACKEND = "school_management.services.email_services.DevEmailBackend"  # Only in dev mode

#EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend" # Console email backend

# if not DEBUG:
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT")
EMAIL_USE_TLS = config("EMAIL_USE_TLS") # bool val
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_USE_LOCALTIME = config("EMAIL_USE_LOCALTIME") # bool val
DEFAULT_FROM_EMAIL = f"{SITE_NAME} <{EMAIL_HOST_USER}>"
SERVER_EMAIL = f"Server Error - {SITE_NAME} <{EMAIL_HOST_USER}>"








#############################################################
#############################################################
#############################################################
#######                                             #########
#######                                             #########
#######                  CACHES CONFIGS             #########
#######                                             #########
#######                                             #########
#############################################################
#############################################################
#############################################################
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache", # or a desired cache's backend. I do prefer this one
        "LOCATION": "Caches",
        "KEY_FUNCTION": "django_tenants.cache.make_key", # Added because of "django-tenants"
        "REVERSE_KEY_FUNCTION": "django_tenants.cache.reverse_key", # Added because of "django-tenants"
    }
}
CACHE_MIDDLEWARE_ALIAS = "default"
CACHE_MIDDLEWARE_SECONDS = 60 * 10 # 10 mins




#############################################################
#############################################################
#############################################################
#######                                             #########
#######                                             #########
#######                 SESSIONS CONFIGS            #########
#######                                             #########
#######                                             #########
#############################################################
#############################################################
#############################################################
SESSION_CACHE_ALIAS = "default"
SESSION_COOKIE_AGE = 604800 # One week
SESSION_COOKIE_NAME = "sessionid"
SESSION_COOKIE_SECURE = False
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = False
SESSION_COOKIE_DOMAIN = ".localhost"

# if PRODUCTION_MODE: # applying prod sessions confs
#     #SESSION_COOKIE_SECURE = True # Use current conf only in production
#     SESSION_COOKIE_HTTPONLY = True # Use current conf only in production
#     #SESSION_COOKIE_DOMAIN = f".{PRODUCTION_MAIN_DOMAIN_NAME}"






#############################################################
#############################################################
#############################################################
#######                                             #########
#######                                             #########
#######                  HTTPS CONFIGS              #########
#######                                             #########
#######                                             #########
#############################################################
#############################################################
#############################################################
# if PRODUCTION_MODE: # applying prod HTTPS/SSL confs
#     SECURE_HSTS_SECONDS = 60 # Use current conf only in production
#     SECURE_HSTS_INCLUDE_SUBDOMAINS = True # Use current conf only in production
#     SECURE_HSTS_PRELOAD = True # Use current conf only in production
#     SECURE_SSL_REDIRECT = True # Use current conf only in production
#     SESSION_COOKIE_SECURE = True # Use current conf only in production
#     CSRF_COOKIE_SECURE = True # Use current conf only in production
#     SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups" # Use current conf only in production















#############################################################
#############################################################
#############################################################
#######                                             #########
#######                                             #########
#######           3rd PARTY APPS CONFIGS            #########
#######                                             #########
#######                                             #########
#############################################################
#############################################################
#############################################################


#############################################################
#############################################################
########          DJANGO TENANTS CONFIGS         ############
#############################################################
#############################################################
BASE_DOMAIN_NAME : str = "localhost" # Domain name on development (CAUTION: define it without protocol or port)

if PRODUCTION_MODE:
    # Real domain name on production. Replace with a real domain name (if any)
    BASE_DOMAIN_NAME = PRODUCTION_MAIN_DOMAIN_NAME # (CAUTION: define it without protocol or port)

TENANT_MODEL = "schools.School" # tenant model
TENANT_DOMAIN_MODEL = "schools.Domain" # tenant domain model
PUBLIC_SCHEMA_URLCONF = "school_management.urls.public_urls" # separating tenant's URLs from public URLs
SHOW_PUBLIC_IF_NO_TENANT_FOUND = True
TENANT_COLOR_ADMIN_APPS = True # or False
AUTO_DROP_SCHEMA = True # or False



#############################################################
#############################################################
########          CELERY & REDIS CONFIGS         ############
#############################################################
#############################################################
REDIS_BROKER_URL = config("REDIS_URL") or "redis://localhost:6379/0" # or a custom broker (then install your own dependencies)
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = "django-cache"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler" # database scheduler or a prefered one


#############################################################
#############################################################
########            SUMMERNOTE CONFIGS           ############
#############################################################
#############################################################
SUMMERNOTE_THEME = "bs4"
SUMMERNOTE_CONFIG = {
    "airMode": False,
    "tabsize": 2,
    "height": 350,
    "width": "100%",
    "focus": True,
    "attachment_require_authentication": True, # Require users to be authenticated for uploading attachments.
    "attachment_absolute_uri": True,
    "lang": None,
    "toolbar": [
        ["style", ["style"]],
        ["font", ["bold", "underline", "clear"]],
        ["color", ["color"]],
        ["para", ["ul", "ol", "paragraph"]],
        ["table", ["table"]],
        ["insert", ["link", "picture", "video"]],
        ["view", ["fullscreen", "codeview", "help"]]
    ],
}


#############################################################
#############################################################
########            REST FRAMEWORK CONFIGS       ############
#############################################################
#############################################################
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
        "rest_framework.permissions.IsAuthenticated",
        "rest_framework.permissions.IsAdminUser",
        # you can add additional permissions here
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 50, # By default (Override it with "limit" query param or anything else if you want)
}


#############################################################
#############################################################
########         CORS ORIGINS CONFIGS            ############
#############################################################
#############################################################
CORS_ALLOW_ALL_ORIGINS = True # or False, then define which origins are trusted
CORS_ALLOW_CREDENTIALS = True # or False, then configure it based on "django-cors-headers" official docs


#############################################################
#############################################################
########            DRF YASG CONFIGS             ############
#############################################################
#############################################################
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Basic": {
            "type": "basic"
        },
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        }
    },
    "VALIDATOR_URL": None, # Comment it to see if swagger schema is valid or not
    "EXCLUDED_MEDIA_TYPES": ["html"],
    "USE_SESSION_AUTH": True,
    "DISPLAY_OPERATION_ID": True,
    "EXCLUDE_NAMESPACES": ["api:api-home"],
}

REDOC_SETTINGS = {
    "NATIVE_SCROLLBARS": True,
}


#############################################################
#############################################################
########           DJANGO HTMLMIN CONFIGS         ###########
#############################################################
#############################################################
HTML_MINIFY = True
KEEP_COMMENTS_ON_MINIFYING = False


#############################################################
#############################################################
########         DJANGO EASY EDIT CONFIGS        ############
#############################################################
#############################################################
DJANGO_EASY_AUDIT_WATCH_REQUEST_EVENTS = False # Do not intercept GET requests
DJANGO_EASY_AUDIT_WATCH_MODEL_EVENTS = True
DJANGO_EASY_AUDIT_WATCH_AUTH_EVENTS = False # Do not intercept AUTH requests


#############################################################
#############################################################
########        DJANGO CKEDITOR 5 CONFIGS        ############
#############################################################
#############################################################
CKEDITOR_5_ALLOW_ALL_FILE_TYPES = True
CKEDITOR_5_UPLOAD_FILE_TYPES = ["png", "jpeg", "pdf", "docx", "zip", "csv", "xlsx", "webp", "pptx"]
CKEDITOR_5_TOOLBAR = {
    "items": [
        "undo", "redo",
        "|", "heading",
        "|", "fontfamily", "fontsize", "fontColor", "fontBackgroundColor",
        "|", "bold", "italic", "strikethrough", "subscript", "superscript", "code",
        "|", "link", "uploadImage", "blockQuote", "codeBlock",
        "|", "bulletedList", "numberedList", "todoList", "outdent", "indent",
        "|", "insertTable",
        "|", "imageUpload", "fileUpload",
        "|", "alignment",
        "|", "mediaEmbed", "removeFormat", "fontBackgroundColor", "sourceEditing", "insertImage", "highlight",
        # "|", "fullScreen", "codeView", "help",
    ],
    "shouldNotGroupWhenFull": True,
}

CKEDITOR_5_CONFIGS = {
    "default": {
        "language": "fr",
        "additionalLanguages": "all",
        "toolbar": CKEDITOR_5_TOOLBAR,
        "table": {
            "defaultHeadings": {"rows": 1, "columns": 1},
            "contentToolbar": ["tableColumn", "tableRow", "mergeTableCells"],
        },
        "htmlSupport": {
            "allow": [
                {"name": "/.*/", "attributes": True, "classes": True, "styles": True}
            ]
        },
        "list": {
            "properties": {
                "styles": "true",
                "startIndex": "true",
                "reversed": "true",
            }
        },
        "image": {
            "toolbar": ["imageTextAlternative", "|", "imageStyle:alignLeft", "imageStyle:alignRight", "imageStyle:alignCenter", "imageStyle:side",  "|"],
            "styles": ["full", "side", "alignLeft", "alignRight", "alignCenter"]
        },
    },
}


#############################################################
#############################################################
########        DJANGO CRISPY FORM CONFIGS       ############
#############################################################
#############################################################
CRISPY_TEMPLATE_PACK = "bootstrap4"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
