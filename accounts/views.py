from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect

from accounts.models import User


# Create your views here.

def activate_user(request):
    token = request.GET.get('token')
    user_id = request.GET.get('user_id')
    try:
        user = User.objects.get(pk=user_id)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        user = None
    except Exception as e:
        user = None
    if user is None:
        messages.error(request, 'User does not exist')
        return redirect("/")

    if user.is_active:
        messages.success(request, 'This account is already activated')
        return redirect("/login")

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Account activated')
        return redirect("/login")
    else:
        messages.error(request, 'Invalid token')
        return redirect("/")