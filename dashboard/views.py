from django.shortcuts import render


def dashboard_home_view(request):
    context = {}
    template_name = "dashboard/home.html"
    return render(request, template_name, context)
