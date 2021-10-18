from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Opportunity, Contact, Stage
from .models import opportunities, stages, contacts, events, regular_user, admin_user
from datetime import datetime


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
    print("adding opp")
    if not request.session.get("role", False):
        return render(request,
                      "jobber/opportunities/home-alt.html")

    if request.method == 'POST':
        id = max([i.id for i in opportunities]) + 1
        stage = request.POST.get('stage')
        application_link = request.POST.get('application-link')
        title = request.POST.get('title')
        company = request.POST.get('company')
        location = request.POST.get('title')
        recruiter_contact = request.POST.get('recruiter-contact')
        filename_resume = request.POST.get('filename-resume')
        filename_cover = request.POST.get('filename-cover')
        referral_contact = request.POST.get('referral-contact')
        interview_location = request.POST.get('interview-location')
        interview_date = request.POST.get('interview-date')
        o = Opportunity(id=id, create_date=datetime.now(), modified_date=datetime.now(), stage=None, title=title,
                        company=company,
                        location=location, recruiter_contacts=None,
                        application_link=application_link, application=None, referral_contacts=None,
                        interview_location=interview_location, interview_date=interview_date, events=None,
                        next_step=None)
        opportunities.append(o)
        messages.add_message(request, messages.SUCCESS, "Submitted Opportunity: %s, %s" % (title, company))
        # Redirect
        return redirect("opportunities:opportunities_view_item", id)
    else:
        return render(request,
                      "jobber/opportunities/add-item.html",
                      {"stages": stages,
                       "contacts": contacts})


def opportunities_delete_item(request):
    if not request.session.get("role", False):
        return render(request,
                      "jobber/opportunities/home-alt.html")

    id = request.POST.get("id")
    title = request.POST.get("title")
    company = request.POST.get("company")
    if request.method == 'POST':
        for index, opp in enumerate(opportunities):
            if str(opp.id) == id:
                del opportunities[index]
                break
        messages.add_message(request, messages.SUCCESS, "Deleted Opportunity: %s, %s" % (title, company))
        # Redirect
        return redirect("opportunities:opportunities_list")
    else:
        return render(request,
                      "jobber/opportunities/add-item.html",
                      {"stages": stages,
                       "contacts": contacts})


def opportunities_add_contact(request, opportunity_id = None):
    print('adding contact')
    if not request.session.get("role", False):
        return render(request,
                      "jobber/opportunities/home-alt.html")
    if request.method == 'POST':
        id = max([i.id for i in opportunities]) + 1
        form_name = request.POST.get("formname")
        name = request.POST.get("contact-add-name")
        title = request.POST.get("contact-add-title")
        company = request.POST.get("contact-add-company")
        phone = request.POST.get("contact-add-phone")
        email = request.POST.get("contact-add-email")
        c = Contact(id=id,
                    name=name,
                    title=title,
                    company=company,
                    phone_number=phone,
                    email=email)
        contacts.append(c)

    my_opp = None
    for opp in opportunities:
        if opp.id == opportunity_id:
            my_opp = opp
            break

    return render(request,
                  "jobber/opportunities/add-item.html",
                  {"opportunity": my_opp,
                   'stages': stages,
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
