import pytz
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
from .models import regular_user, admin_user, Opportunity, Event, Stage, Contact, User


# Create helper functions
def format_date(date):
    """ Formats date into yyyy-mm-dd format or None when empty"""
    utc = pytz.utc
    if date != '':
        date = utc.localize(datetime.strptime(date, '%Y-%m-%d'))
    else:
        date = None
    return date


def generate_opportunity(request, opportunity_id=None) -> Opportunity:
    """ Creates a new or edits an existing Opportunity object given a request with opportunity form data"""
    utc = pytz.utc
    contacts = Contact.objects.all()
    stage = request.POST.get('stage')
    input_stage = Stage.objects.get(value_name=stage)
    application_link = request.POST.get('application-link')
    title = request.POST.get('title')
    company = request.POST.get('company')
    location = request.POST.get('location')
    recruiter_contact = request.POST.get('REC')
    input_recruiter_contact = None
    if recruiter_contact != '' and recruiter_contact is not None and recruiter_contact != 'none':
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
        my_opp = Opportunity(user=User.objects.get(username=request.session['username']),
                             create_date=utc.localize(datetime.now()), modified_date=utc.localize(datetime.now()),
                             stage=input_stage, title=title,
                             company=company,
                             location=location,
                             application_link=application_link, recruiter_contact=input_recruiter_contact,
                             application=None,
                             interview_location=interview_location, interview_date=interview_date,
                             next_step='')
    else:
        my_opp = Opportunity.objects.get(pk=opportunity_id)
        my_opp.user = User.objects.get(username=request.session['username'])
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
    """ Dashboard view, which instead redirects to promo home page when nobody is logged in """
    if not request.session.get("role", False):
        return render(request,
                      "jobber/opportunities/home-alt.html")
    if request.session['role'] == "admin":
        opportunities = Opportunity.objects.all()
        events = Event.objects.all()
    else:
        opportunities = Opportunity.objects.filter(user=User.objects.get(username=request.session['username']).id)
        events = Event.objects.filter(user=User.objects.get(username=request.session['username']).id)
    return render(request,
                  "jobber/opportunities/index.html",
                  {"user": User.objects.get(username=request.session['username']),
                   "opportunities": opportunities,
                   "events": events})


def opportunities_home_alt(request):
    """ The promo home page, which instead renders the dashboard when logged in"""
    if not request.session.get("role", False):
        return render(request,
                      "jobber/opportunities/home-alt.html")
    if request.session['role'] == "admin":
        opportunities = Opportunity.objects.all()
        events = Event.objects.all()
    else:
        opportunities = Opportunity.objects.filter(user=User.objects.get(username=request.session['username']).id)
        events = Event.objects.filter(user=User.objects.get(username=request.session['username']).id)
    return render(request,
                  "jobber/opportunities/index.html",
                  {"user": User.objects.get(username=request.session['username']),
                   "opportunities": opportunities,
                   "events": events})


def opportunities_list(request):
    """ List of opportunities """
    if not request.session.get("role", False):
        return render(request,
                      "jobber/opportunities/home-alt.html")

    if request.session['role'] == "admin":
        opportunities = Opportunity.objects.all()
    else:
        opportunities = Opportunity.objects.filter(user=User.objects.get(username=request.session['username']).id)
    opportunities = opportunities.order_by('-modified_date')
    stages = Stage.objects.all()
    return render(request,
                  "jobber/opportunities/list.html",
                  {"user": User.objects.get(username=request.session['username']),
                   "opportunities": opportunities,
                   "stages": stages}
                  )


def opportunities_view_item(request, id):
    """ Detail page of a single opportunity, given the opportunity id """
    if not request.session.get("role", False):
        return render(request,
                      "jobber/opportunities/home-alt.html")
    stages = Stage.objects.all()
    my_opp = Opportunity.objects.get(pk=id)
    if request.session['role'] != "admin" and my_opp.user.username != request.session['username']:
        # TODO: Add message denying access
        return redirect("opportunities:opportunities_list")

    return render(request,
                  "jobber/opportunities/view-item.html",
                  {"user": User.objects.get(username=request.session['username']),
                   "opportunity": my_opp,
                   'stages': stages})


def opportunities_edit_item(request, id):
    """ Renders an existing opportunity's details to an editable form, saves inputs on POST request"""
    if not request.session.get("role", False):
        return render(request,
                      "jobber/opportunities/home-alt.html")
    stages = Stage.objects.all()
    my_opp = Opportunity.objects.get(pk=id)
    if request.session['role'] != "admin" and my_opp.user.username != request.session['username']:
        # TODO: Add message denying access
        return redirect("opportunities:opportunities_list")
    if request.method == 'POST':
        my_opp = generate_opportunity(request=request, opportunity_id=id)
        messages.add_message(request, messages.INFO, "Saved Opportunity: %s, %s" % (my_opp.title, my_opp.company))
        return redirect("opportunities:opportunities_view_item", my_opp.id)
    return render(request,
                  "jobber/opportunities/add-item.html",
                  {"user": User.objects.get(username=request.session['username']),
                   "opportunity": my_opp,
                   'stages': stages,
                   "recruiter_contacts": Contact.objects.filter(contact_type='REC'),
                   "referral_contacts": Contact.objects.filter(contact_type='REF')
                   })


def opportunities_add_item(request):
    """ Renders an empty opportunity form page, saves a new Opportunity on POST request"""
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
                      {"user": User.objects.get(username=request.session['username']),
                       "stages": stages,
                       "recruiter_contacts": Contact.objects.filter(contact_type='REC'),
                       "referral_contacts": Contact.objects.filter(contact_type='REF')
                       })


def opportunities_delete_item(request):
    """ Deletes an Opportunity given a POST request with the opportunity id to be deleted"""
    if not request.session.get("role", False):
        return render(request,
                      "jobber/opportunities/home-alt.html")

    if request.method == 'POST':
        opportunity_id = request.POST.get("id")
        my_opp = Opportunity.objects.get(pk=opportunity_id)
        if request.session['role'] != "admin" and my_opp.user.username != request.session['username']:
            # TODO: Add message denying access
            return redirect("opportunities:opportunities_list")
        title = my_opp.title
        company = my_opp.company
        my_opp.delete()
        messages.add_message(request, messages.WARNING, "Deleted Opportunity: %s, %s" % (title, company))
        # Redirect
        return redirect("opportunities:opportunities_list")
    else:
        stages = Stage.objects.all()
        return render(request,
                      "jobber/opportunities/add-item.html",
                      {"user": User.objects.get(username=request.session['username']),
                       "stages": stages,
                       "recruiter_contacts": Contact.objects.filter(contact_type='REC'),
                       "referral_contacts": Contact.objects.filter(contact_type='REF')
                       })


def opportunities_add_contact_ajax(request):
    """ Adds a Contact sent from an AJAX POST request"""
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == "POST":
        form_name = request.POST.get("formname")
        name = request.POST.get("contact_add_name")
        title = request.POST.get("contact_add_title")
        company = request.POST.get("contact_add_company")
        phone = request.POST.get("contact_add_phone")
        email = request.POST.get("contact_add_email")
        try:
            my_contact = Contact(
                user=User.objects.get(username=request.session['username']),
                name=name,
                title=title,
                company=company,
                phone_number=phone,
                email=email,
                contact_type=form_name)
            my_contact.save()
            new_contact_id = my_contact.id
            return JsonResponse(
                {'success': 'success', 'contact_type': form_name, 'contact_id': new_contact_id, 'contact_name': name},
                status=200)
        except:
            return JsonResponse(
                {'error': 'Data types entered are invalid.'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid request.'}, status=400)


def opportunities_view_contact_ajax(request):
    """ Returns a Contact's details sent from an AJAX GET request, given a Contact id"""
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == "GET":
        contact_id = int(request.GET.get("contact_id"))
        try:
            my_contact = Contact.objects.get(pk=contact_id)
            contact_name = my_contact.name
            contact_title = my_contact.title
            contact_company = my_contact.company
            contact_phone = my_contact.phone_number
            contact_email = my_contact.email
            return JsonResponse(
                {'success': 'success', 'contact_name': contact_name, 'contact_title': contact_title,
                 'contact_company': contact_company,
                 'contact_phone': contact_phone,
                 'contact_email': contact_email},
                status=200)
        except:
            return JsonResponse(
                {'error': 'Contact not found.'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request.'}, status=400)


def opportunities_list_sort_ajax(request):
    """ Returns the sorted index of Opportunity items sent from an AJAX GET request, given a sorter name"""
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == "GET":
        sorter = request.GET.get("sorter")
        try:
            opportunities = Opportunity.objects.filter(user=User.objects.get(username=request.session['username']).id)
            if sorter == "modified-date":
                opportunities = opportunities.order_by("-modified_date")
            elif sorter == "created-date":
                opportunities = opportunities.order_by("-created_date")
            elif sorter == "stage":
                opportunities = opportunities.order_by("stage__id")

            opp_order = {}
            for index, opp in enumerate(opportunities):
                opp_order[str(index)] = opp.id
            return JsonResponse(
                {'success': 'success', 'opportunities': opp_order},
                status=200)
        except:
            return JsonResponse(
                {'error': 'Contact not found.'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request.'}, status=400)


def opportunities_add_contact(request):
    """ Creates a new contact """
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
        my_contact = Contact(
            user=User.objects.get(username=request.session['username']),
            name=name,
            title=title,
            company=company,
            phone_number=phone,
            email=email,
            contact_type=form_name)
        my_contact.save()

    return redirect("opportunities:opportunities_index")


def opportunities_search_results(request):
    """ Renders the search page """
    return render(request,
                  "jobber/opportunities/search-results.html")


def login(request):
    """ Login """
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
    """ Logout """
    del request.session['username']
    del request.session['role']
    return redirect("opportunities:opportunities_index")
