from django.contrib.auth import authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from actions.models import Action


# Helper functions
def get_profile(request):
    return Profile.objects.get(user__username=request.session['username'])


def generate_profile(request, profile_id) -> Profile:
    """ Creates a new or edits an existing Profile object given a request with profile form data"""
    first_name = request.POST.get("input-name1")
    last_name = request.POST.get("input-name2")
    email = request.POST.get("input-email")
    if User.objects.exclude(pk=profile_id).filter(email=email).exists():
        messages.add_message(request, messages.WARNING,
                             "The email %s is already in use.  Please select another and try again" % email)
        return None
    password = request.POST.get("input-password")
    is_public = request.POST.get("input-public")
    if is_public == "on":
        is_public = True
    else:
        is_public = False
    my_profile = Profile.objects.get(pk=profile_id)
    my_user = my_profile.user
    my_user.first_name = first_name
    my_user.last_name = last_name
    my_user.email = email
    if password != '':
        my_user.set_password(password)
    my_profile.is_public = is_public
    my_profile.save()
    my_user.save()
    return my_profile


# Create your views here.
def register(request):
    if request.session.get("role", False):
        return redirect("jobber:opportunities_index")
    if request.method == 'POST':
        username = request.POST.get('register-username')
        first_name = request.POST.get('register-name1')
        last_name = request.POST.get('register-name2')
        email = request.POST.get('register-email')
        password = request.POST.get('register-password')
        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.WARNING,
                                 "The username %s is already in use.  Please select another and try again" % username)
            return redirect("users:register")
        if User.objects.filter(email=email).exists():
            messages.add_message(request, messages.WARNING,
                                 "The email %s is already in use.  Please select another and try again" % email)
            return redirect("users:register")
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
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
                  "users/user/view-item.html",
                  {"user": get_profile(request),
                   "profile": user1.profile,
                   "actions": actions})


def profiles_edit_item(request, username):
    """ Renders an existing profile's details to an editable form, saves inputs on POST request"""
    if not request.session.get("role", False):
        return render(request,
                      "jobber/home-alt.html")
    my_profile = get_object_or_404(User, username=username).profile
    if request.session['role'] != "admin" and my_profile.user.username != request.session['username']:
        # TODO: Add message denying access
        return redirect("jobber:profile", username=my_profile.user.username)
    if request.method == 'POST':
        my_profile = generate_profile(request=request, profile_id=my_profile.id)
        if my_profile is not None:
            action = Action(
                user=get_profile(request),
                verb="updated profile",
                target=my_profile
            )
            action.save()
            messages.add_message(request, messages.INFO, "Updated Profile")
            return redirect("users:profile", my_profile.user.username)
        else:
            print("post", username)
            return redirect("users:profiles_edit_item", username=username)
    return render(request,
                  "users/user/add-item.html",
                  {"user": get_profile(request),
                   "profile": my_profile,
                   })


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
