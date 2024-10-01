from dashboard import views
from django.urls import path

app_name = "dashboard"

urlpatterns = [
    path("", views.dashboard_home_view, name="home"),
]
