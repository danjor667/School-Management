from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required

from accounts.models import User
from django_tenants.utils import schema_context
from schools.models import School

from schools.forms import CreateSchoolForm
from schools.serializers import SchoolSerializer
from schools.after_response import create_school_schema_and_domain_task
from students.models import Student
from teachers.models import Teacher
from tenant_users.models import TenantUser
from utilities.utils import redirect_to_tenant_domain


def index(request):
    return render(request, "index.html", {})


def register(request):  # register student or teacher in the relevant tenant schema
    if request.method == "POST":
        data = request.POST
        email = data.get("email")
        password = data.get("password")
        code = data.get("code")
        school = School.objects.get(badge=code.split("-")[0])

        if school:
            with schema_context(school.schema_name):
                user = TenantUser.objects.create_tenant_user(email=email, password=password)
                user.save()
                if code.endswith("-STUDENT"):
                    student = Student.objects.create(user=user)
                    student.save()
                    messages.success(request, _("You have successfully registered."))
                elif code.endswith("-TEACHER"):
                    teacher = Teacher.objects.create(user=user)
                    teacher.save()
                    messages.success(request, _("You have successfully registered."))
                else:
                    messages.error(request, _("Please enter a valid code!"))
        else:
            messages.error(request, _("the code is invalid!."))
    return render(request, "user/signup.html", {})


def _login(request):  # login student or teacher
    if request.method == "POST":
        data = request.POST
        email = data.get("email")
        password = data.get("password")
        user = authenticate(email=email, password=password)
        if user:
            with schema_context(user.tenant.schema_name):
                login(request, user)
                return redirect_to_tenant_domain(user)
        else:
            messages.error(request, _("Invalid email or password."))
            return render(request, "user/login.html", {})
    return render(request, "user/login.html", {})


# @login_required  # update login url later on
def create_school_view(request):
    form = CreateSchoolForm()

    if request.method == "POST":
        form = CreateSchoolForm(data=request.POST, files=request.FILES) or None
        if form.is_valid():
            cleaned_data = form.cleaned_data
            school = School(**cleaned_data)

            # serialize data in order to be able to transform it into a dict
            serialized_data = SchoolSerializer(school, many=False).data

            # submit creation process using a background task
            create_school_schema_and_domain_task.after_response(
                request=request,
                data=dict(serialized_data),  # transform data to dict
                submited_by=request.user
            )

            # processing, send a feedback
            messages.success(request, _("École en cours de création. Veuillez patienter s'il vous plaît !"))
            return redirect("/")  # redirect to current page again (should be changed later on)

        else:  # if not form.is_valid()
            errors = form.errors.as_data()
            for error in errors:
                msg = "".join(errors[error][0])
                messages.error(request, _(f"{msg}"))
            return redirect("/")

    context = {
        "form": form
    }
    template_name = "create_school.html"
    return render(request, template_name, context)


##################################################################################################


def create_register(request):  # register principal of the school
    if request.method == "POST":
        data = request.POST
        email = data.get("email")
        password = data.get("password")
        code = data.get("code")
        user = User.objects.create_user(email=email, password=password)  #create either teacher or student base on code
        user = user.save()
        return redirect("/create-login/")
    return render(request, "principal/admin_register.html", {})


def create_login(request):  ## log in the principal of a school for him to be able to register a school
    if request.method == "POST":
        data = request.POST
        email = data.get("email")
        password = data.get("password")
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("/create-school")
    return render(request, "principal/admin_login.html", {})