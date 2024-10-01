from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.views.static import serve
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from django.contrib.sitemaps import views as sitemap_views


# DJANGO ADMIN URLs
urlpatterns = [
    path(f"admin/admindocs/", include("django.contrib.admindocs.urls")), # Must appear before admin.site.urls
    path(f"admin/", admin.site.urls),
]

# 3rd PARTY APPS URLs
urlpatterns += [
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("summernote/", include("django_summernote.urls")),
    path("hitcount/", include("hitcount.urls", namespace="hitcount")),
]

# Only dev mode URLs
if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]





# LOCALE APPS URLs (public schemas URLs)
urlpatterns += [
    path("", include("schools.urls", namespace="schools")),
]





# Serving static and media files (adding them to project URL)
urlpatterns += static(settings.STATIC_URL, serve, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, serve, document_root=settings.MEDIA_ROOT)
