from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def register(request):
    if request.session.get("role", False):
        return redirect("opportunities:opportunities_index")
    if request.method == 'POST':
        username = request.POST.get('register-username')
        email = request.POST.get('register-email')
        password = request.POST.get('register-password')
        user = User.objects.create_user(username, email, password)
        messages.add_message(request, messages.SUCCESS, "Welcome, %s" % user.username)
        return redirect('opportunities:opportunities_index')

    return render(request,
                  "users/user/register.html",)