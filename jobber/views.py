from django.shortcuts import render, redirect
from .models import opportunities, stages, contacts, events, regular_user, admin_user


# Create your views here.
def opportunities_index(request):
    if not request.session.get("role", False):
        return render(request,
                      "jobber/opportunities/home-alt.html")
    return render(request,
                  "jobber/opportunities/index.html",
                  {"opportunities": opportunities,
                   "events": events})


def opportunities_home_alt(request):
    if not request.session.get("role", False):
        return render(request,
                      "jobber/opportunities/home-alt.html")
    return render(request,
                  "jobber/opportunities/index.html",
                  {"opportunities": opportunities,
                   "events": events})


def opportunities_list(request):
    if not request.session.get("role", False):
        return render(request,
                      "jobber/opportunities/home-alt.html")
    return render(request,
                  "jobber/opportunities/list.html",
                  {"opportunities": opportunities}
                  )


def opportunities_view_item(request, id):
    if not request.session.get("role", False):
        return render(request,
                      "jobber/opportunities/home-alt.html")
    my_opp = None
    for opp in opportunities:
        if opp.id == id:
            my_opp = opp
            break
    return render(request,
                  "jobber/opportunities/view-item.html",
                  {"opportunity": my_opp,
                   'stages': stages})


def opportunities_edit_item(request, id):
    if not request.session.get("role", False):
        return render(request,
                      "jobber/opportunities/home-alt.html")
    my_opp = None
    for opp in opportunities:
        if opp.id == id:
            my_opp = opp
            break
    return render(request,
                  "jobber/opportunities/add-item.html",
                  {"opportunity": my_opp,
                   'stages': stages,
                   "contacts": contacts})


def opportunities_add_item(request):
    if not request.session.get("role", False):
        return render(request,
                      "jobber/opportunities/home-alt.html")
    return render(request,
                  "jobber/opportunities/add-item.html",
                  {"stages": stages,
                   "contacts": contacts})


def opportunities_search_results(request):
    return render(request,
                  "jobber/opportunities/search-results.html")

def login(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    if (username == regular_user["username"]) & (password == regular_user["password"]):
        request.session['username'] = username
        request.session['role'] = 'regular'
    elif (username == admin_user["username"]) & (password == admin_user["password"]):
        request.session['username'] = username
        request.session['role'] = 'admin'
    return redirect("opportunities:opportunities_index")

def logout(request):
    del request.session['username']
    del request.session['role']
    return redirect("opportunities:opportunities_index")