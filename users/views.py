from django.contrib.auth import authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from actions.models import Action


# Helper functions
def get_profile(request):
    return Profile.objects.get(user__username=request.session['username'])


# Create your views here.
def register(request):
    if request.session.get("role", False):
        return redirect("jobber:opportunities_index")
    if request.method == 'POST':
        username = request.POST.get('register-username')
        email = request.POST.get('register-email')
        password = request.POST.get('register-password')
        user = User.objects.create_user(username, email, password)
        request.session['username'] = user.username
        request.session['role'] = user.profile.role
        messages.add_message(request, messages.SUCCESS, "Welcome, %s" % user.username)
        return redirect("jobber:opportunities_index")

    return render(request,
                  "users/user/register.html")


def profile(request, username):
    user1 = get_object_or_404(User, username=username)
    actions = Action.objects.filter(
        user=Profile.objects.get(user__username=username)).order_by("-created")[:10]
    if request.method == 'POST':
        pass
    return render(request,
                  "users/user/view-profile.html",
                  {"user": user1.profile,
                   "actions": actions})


def login_user(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(username=username, password=password)
    if user is not None:
        request.session['username'] = user.username
        request.session['role'] = user.profile.role
        messages.add_message(request, messages.SUCCESS,
                             "Welcome back, %s" % user.username)
    else:
        messages.add_message(request, messages.ERROR,
                             "Invalid username or password")
    return redirect("jobber:opportunities_index")


def logout_user(request):
    del request.session['username']
    del request.session['role']
    return redirect("jobber:opportunities_index")
