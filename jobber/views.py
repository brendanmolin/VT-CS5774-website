import pytz
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from .models import regular_user, admin_user, Opportunity, Event, Stage, Contact


# Create helper functions
def format_date(date):
    utc = pytz.utc
    if date != '':
        date = utc.localize(datetime.strptime(date, '%Y-%m-%d'))
    else:
        date = None
    return date


def generate_opportunity(request, opportunity_id=None) -> Opportunity:
    utc = pytz.utc
    contacts = Contact.objects.all()
    stage = request.POST.get('stage')
    input_stage = Stage.objects.get(value_name=stage)
    print(input_stage)
    application_link = request.POST.get('application-link')
    title = request.POST.get('title')
    company = request.POST.get('company')
    location = request.POST.get('location')
    recruiter_contact = request.POST.get('REC')
    input_recruiter_contact = None
    if recruiter_contact is not '':
        input_recruiter_contact = Contact.objects.get(pk=recruiter_contact)
    filename_resume = request.POST.get('filename-resume')
    filename_cover = request.POST.get('filename-cover')
    referral_contact = request.POST.getlist('REF')
    referral_contact_inputs = []
    for c in contacts:
        if str(c.id) in referral_contact:
            referral_contact_inputs.append(c)
    interview_location = request.POST.get('interview-location')
    interview_date = request.POST.get('interview-date')
    interview_date = format_date(interview_date)
    if opportunity_id is None:
        my_opp = Opportunity(create_date=utc.localize(datetime.now()), modified_date=utc.localize(datetime.now()),
                             stage=input_stage, title=title,
                             company=company,
                             location=location,
                             application_link=application_link, recruiter_contact=input_recruiter_contact,
                             application=None,
                             interview_location=interview_location, interview_date=interview_date,
                             next_step='')
    else:
        my_opp = Opportunity.objects.get(pk=opportunity_id)
        my_opp.modified_date = utc.localize(datetime.now())
        my_opp.stage = input_stage
        my_opp.title = title
        my_opp.company = company
        my_opp.location = location
        my_opp.application_link = application_link
        my_opp.recruiter_contact = input_recruiter_contact
        my_opp.application = None
        my_opp.interview_location = interview_location
        my_opp.interview_date = interview_date
        my_opp.next_step = ''
    my_opp.save()
    my_opp.referral_contacts.clear()
    for c in referral_contact_inputs:
        my_opp.referral_contacts.add(c)
    my_opp.save()
    return my_opp


# Create your views here.
def opportunities_index(request):
    if not request.session.get("role", False):
        return render(request,
                      "jobber/opportunities/home-alt.html")
    opportunities = Opportunity.objects.all()
    events = Event.objects.all()
    return render(request,
                  "jobber/opportunities/index.html",
                  {"opportunities": opportunities,
                   "events": events})


def opportunities_home_alt(request):
    if not request.session.get("role", False):
        return render(request,
                      "jobber/opportunities/home-alt.html")
    opportunities = Opportunity.objects.all()
    events = Event.objects.all()
    return render(request,
                  "jobber/opportunities/index.html",
                  {"opportunities": opportunities,
                   "events": events})


def opportunities_list(request):
    if not request.session.get("role", False):
        return render(request,
                      "jobber/opportunities/home-alt.html")
    opportunities = Opportunity.objects.all()
    stages = Stage.objects.all()
    return render(request,
                  "jobber/opportunities/list.html",
                  {"opportunities": opportunities,
                   "stages": stages}
                  )


def opportunities_view_item(request, id):
    if not request.session.get("role", False):
        return render(request,
                      "jobber/opportunities/home-alt.html")
    stages = Stage.objects.all()
    my_opp = Opportunity.objects.get(pk=id)
    return render(request,
                  "jobber/opportunities/view-item.html",
                  {"opportunity": my_opp,
                   'stages': stages})


def opportunities_edit_item(request, id):
    if not request.session.get("role", False):
        return render(request,
                      "jobber/opportunities/home-alt.html")
    stages = Stage.objects.all()
    my_opp = Opportunity.objects.get(pk=id)
    if request.method == 'POST':
        my_opp = generate_opportunity(request=request, opportunity_id=id)
        messages.add_message(request, messages.SUCCESS, "Saved Opportunity: %s, %s" % (my_opp.title, my_opp.company))
    return render(request,
                  "jobber/opportunities/add-item.html",
                  {"opportunity": my_opp,
                   'stages': stages,
                   "recruiter_contacts": Contact.objects.filter(contact_type='REC'),
                   "referral_contacts": Contact.objects.filter(contact_type='REF')
                   })


def opportunities_add_item(request):
    if not request.session.get("role", False):
        return render(request,
                      "jobber/opportunities/home-alt.html")

    stages = Stage.objects.all()
    if request.method == 'POST':
        my_opp = generate_opportunity(request, opportunity_id=None)
        messages.add_message(request, messages.SUCCESS,
                             "Submitted Opportunity: %s, %s" % (my_opp.title, my_opp.company))
        # Redirect
        return redirect("opportunities:opportunities_view_item", my_opp.id)
    else:
        return render(request,
                      "jobber/opportunities/add-item.html",
                      {"stages": stages,
                       "recruiter_contacts": Contact.objects.filter(contact_type='REC'),
                       "referral_contacts": Contact.objects.filter(contact_type='REF')
                       })


def opportunities_delete_item(request):
    if not request.session.get("role", False):
        return render(request,
                      "jobber/opportunities/home-alt.html")

    if request.method == 'POST':
        opportunity_id = request.POST.get("id")
        my_opp = Opportunity.objects.get(pk=opportunity_id)
        title = my_opp.title
        company = my_opp.company
        my_opp.delete()
        messages.add_message(request, messages.SUCCESS, "Deleted Opportunity: %s, %s" % (title, company))
        # Redirect
        return redirect("opportunities:opportunities_list")
    else:
        stages = Stage.objects.all()
        return render(request,
                      "jobber/opportunities/add-item.html",
                      {"stages": stages,
                       "recruiter_contacts": Contact.objects.filter(contact_type='REC'),
                       "referral_contacts": Contact.objects.filter(contact_type='REF')
                       })


def opportunities_add_contact(request):
    if not request.session.get("role", False):
        return render(request,
                      "jobber/opportunities/home-alt.html")
    if request.method == 'POST':
        form_name = request.POST.get("formname")
        name = request.POST.get("contact-add-name")
        title = request.POST.get("contact-add-title")
        company = request.POST.get("contact-add-company")
        phone = request.POST.get("contact-add-phone")
        email = request.POST.get("contact-add-email")
        my_contact = Contact(name=name,
                             title=title,
                             company=company,
                             phone_number=phone,
                             email=email,
                             contact_type=form_name)
        my_contact.save()

    return redirect("opportunities:opportunities_index")


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
