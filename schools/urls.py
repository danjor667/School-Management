import accounts.views
from schools import views
from django.urls import path

from utilities.utils import generate_activation_link

app_name = "schools"

urlpatterns = [
    # path("create-school/", views.create_school_view, name="create-school"),
    path("", views.index, name="create-school"),
    path("login/", views._login, name="login"),
    path('register/', views.register, name="register"),

    path('create-login/', views.create_login, name="create_login"),
    path('create-register/', views.create_register, name="create_register"),
    path("create-school/", views.create_school_view, name="create-school"),
    path("activate-user/", accounts.views.activate_user, name="activate_user"),

]