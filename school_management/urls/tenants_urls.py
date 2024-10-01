import notifications.urls

from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.views.static import serve
from django.conf.urls.static import static


# DJANGO ADMIN URLs (tenant schemas)
urlpatterns = [
    path(f"admin/admindocs/", include("django.contrib.admindocs.urls")), # Must appear before admin.site.urls
    path(f"admin/", admin.site.urls),
]


# 3rd PARTY APPS URLs
urlpatterns += [
    path("summernote/", include("django_summernote.urls")),
    path("hitcount/", include("hitcount.urls", namespace="hitcount")),
    path("notifications-hq/", include(notifications.urls, namespace="notifications")),
]


# LOCALE TENANTS APPS URLs
urlpatterns += [
    path("", include("dashboard.urls", namespace="dashboard")),
]



# Only dev mode URLs
if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]



# Serving static and media files (adding them to project URL)
urlpatterns += static(settings.STATIC_URL, serve, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, serve, document_root=settings.MEDIA_ROOT)
