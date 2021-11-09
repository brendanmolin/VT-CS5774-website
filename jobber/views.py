import pytz
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
from .models import Opportunity, Event, Stage, Contact
from users.models import Profile
from actions.models import Action


# Create helper functions
def format_date(date):
    """ Formats date into yyyy-mm-dd format or None when empty"""
    utc = pytz.utc
    if date != '':
        date = utc.localize(datetime.strptime(date, '%Y-%m-%d'))
    else:
        date = None
    return date


def get_profile(request):
    return Profile.objects.get(user__username=request.session['username'])


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
    if opportunity_id is None:
        my_opp = Opportunity(profile=get_profile(request),
                             create_date=utc.localize(datetime.now()), modified_date=utc.localize(datetime.now()),
                             stage=input_stage, title=title,
                             company=company,
                             location=location,
                             application_link=application_link, recruiter_contact=input_recruiter_contact,
                             application=None,
                             next_step='')
    else:
        my_opp = Opportunity.objects.get(pk=opportunity_id)
        my_opp.profile = get_profile(request)
        my_opp.modified_date = utc.localize(datetime.now())
        my_opp.stage = input_stage
        my_opp.title = title
        my_opp.company = company
        my_opp.location = location
        my_opp.application_link = application_link
        my_opp.recruiter_contact = input_recruiter_contact
        my_opp.application = None
        my_opp.next_step = ''
    my_opp.save()
    my_opp.referral_contacts.clear()
    for c in referral_contact_inputs:
        my_opp.referral_contacts.add(c)
    my_opp.save()
    return my_opp


def generate_contact(request, contact_id=None) -> Contact:
    """ Creates a new or edits an existing Contact object given a request with contact form data"""
    utc = pytz.utc
    contact_type = request.POST.get("contact-type")
    name = request.POST.get("contact-name")
    title = request.POST.get("contact-title")
    company = request.POST.get("contact-company")
    phone = request.POST.get("contact-phone")
    email = request.POST.get("contact-email")
    if contact_id is None:
        my_contact = Contact(
            profile=get_profile(request),
            name=name,
            title=title,
            company=company,
            phone_number=phone,
            email=email,
            contact_type=contact_type)
    else:
        my_contact = Contact.objects.get(pk=contact_id)
        my_contact.profile = get_profile(request)
        my_contact.modified_date = utc.localize(datetime.now())
        my_contact.name = name
        my_contact.title = title
        my_contact.company = company
        my_contact.phone_number = phone
        my_contact.email = email
        my_contact.contact_type = contact_type
    my_contact.save()
    return my_contact


def generate_event(request, event_id=None) -> Event:
    """ Creates a new or edits an existing Event object given a request with event form data"""
    utc = pytz.utc
    date = request.POST.get("input-date")
    title = request.POST.get("input-title")
    e_type = request.POST.get("input-type")
    opp = request.POST.getlist("input-opp")
    if event_id is None:
        my_event = Event(
            profile=get_profile(request),
            date=format_date(date),
            title=title,
            type=e_type)
    else:
        my_event = Event.objects.get(pk=event_id)
        my_event.profile = get_profile(request)
        my_event.date = date
        my_event.title = title
        my_event.type = e_type
    my_event.save()
    for o in opp:
        if o == "none":
            continue
        my_opp = Opportunity.objects.get(pk=o)
        my_opp.events.clear()
        my_opp.events.add(my_event.id)
        my_opp.save()
    return my_event


def get_opportunities_by_user_and_role(request):
    """ Gets permissioned Opportunities """
    if request.session['role'] == "admin":
        opportunities = Opportunity.objects.all()
    else:
        opportunities = Opportunity.objects.filter(
            profile=get_profile(request).id)
    return opportunities


def get_events_by_user_and_role(request):
    """ Gets permissioned Events """
    if request.session['role'] == "admin":
        events = Event.objects.all()
    else:
        events = Event.objects.filter(
            profile=get_profile(request).id)
    return events


def get_contacts_by_user_and_role(request):
    """ Gets permissioned Events """
    if request.session['role'] == "admin":
        contacts = Contact.objects.all()
    else:
        contacts = Contact.objects.filter(
            profile=get_profile(request).id)
    return contacts


def get_actions_by_user_and_role(request):
    """ Gets permissioned Events """
    if request.session['role'] == "admin":
        actions = Action.objects.all()
    else:
        actions = Action.objects.filter(
            user=get_profile(request).id)
    return actions


# Create your views here.

# Main pages
def opportunities_index(request):
    """ Dashboard view, which instead redirects to promo home page when nobody is logged in """
    if not request.session.get("role", False):
        return render(request,
                      "jobber/home-alt.html")
    actions = get_actions_by_user_and_role(request).order_by("-created")[:3]
    events = get_events_by_user_and_role(request)
    return render(request,
                  "jobber/index.html",
                  {"user": get_profile(request),
                   "actions": actions,
                   "events": events})


def opportunities_home_alt(request):
    """ The promo home page, which instead renders the dashboard when logged in"""
    if not request.session.get("role", False):
        return render(request,
                      "jobber/home-alt.html")
    opportunities = get_opportunities_by_user_and_role(request)
    events = get_events_by_user_and_role(request)
    return render(request,
                  "jobber/index.html",
                  {"user": get_profile(request),
                   "opportunities": opportunities,
                   "events": events})


def opportunities_search_results(request):
    """ Renders the search page """
    return render(request,
                  "jobber/search-results.html")


# Opportunities Views

def opportunities_list(request):
    """ List of opportunities """
    if not request.session.get("role", False):
        return render(request,
                      "jobber/home-alt.html")

    opportunities = get_opportunities_by_user_and_role(request)
    opportunities = opportunities.order_by('-modified_date')
    stages = Stage.objects.all()
    return render(request,
                  "jobber/opportunities/list.html",
                  {"user": get_profile(request),
                   "opportunities": opportunities,
                   "stages": stages}
                  )


def opportunities_list_sort_ajax(request):
    """ Returns the sorted index of Opportunity items sent from an AJAX GET request, given a sorter name"""
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == "GET":
        sorter = request.GET.get("sorter")
        try:
            opportunities = get_opportunities_by_user_and_role(request)
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


def opportunities_view_item(request, id):
    """ Detail page of a single opportunity, given the opportunity id """
    if not request.session.get("role", False):
        return render(request,
                      "jobber/home-alt.html")
    stages = Stage.objects.all()
    my_opp = Opportunity.objects.get(pk=id)
    if request.session['role'] != "admin" and my_opp.profile.user.username != request.session['username']:
        # TODO: Add message denying access
        return redirect("jobber:opportunities_list")

    return render(request,
                  "jobber/opportunities/view-item.html",
                  {"user": get_profile(request),
                   "opportunity": my_opp,
                   'stages': stages})


def opportunities_edit_item(request, id):
    """ Renders an existing opportunity's details to an editable form, saves inputs on POST request"""
    if not request.session.get("role", False):
        return render(request,
                      "jobber/home-alt.html")
    stages = Stage.objects.all()
    my_opp = Opportunity.objects.get(pk=id)
    if request.session['role'] != "admin" and my_opp.profile.user.username != request.session['username']:
        # TODO: Add message denying access
        return redirect("jobber:opportunities_list")
    if request.method == 'POST':
        my_opp = generate_opportunity(request=request, opportunity_id=id)
        # Log Action
        action = Action(
            user=get_profile(request),
            verb="updated opportunity",
            target=my_opp
        )
        action.save()

        messages.add_message(request, messages.INFO, "Saved Opportunity: %s, %s" % (my_opp.title, my_opp.company))
        return redirect("jobber:opportunities_view_item", my_opp.id)
    contacts = get_contacts_by_user_and_role(request)
    return render(request,
                  "jobber/opportunities/add-item.html",
                  {"user": get_profile(request),
                   "opportunity": my_opp,
                   'stages': stages,
                   "recruiter_contacts": contacts.filter(contact_type='REC'),
                   "referral_contacts": contacts.filter(contact_type='REF')
                   })


def opportunities_add_item(request):
    """ Renders an empty opportunity form page, saves a new Opportunity on POST request"""
    if not request.session.get("role", False):
        return render(request,
                      "jobber/home-alt.html")

    stages = Stage.objects.all()
    if request.method == 'POST':
        # Add new opportunity
        my_opp = generate_opportunity(request, opportunity_id=None)
        # Log Action
        action = Action(
            user=get_profile(request),
            verb="created a new opportunity",
            target=my_opp
        )
        action.save()
        # Send success message
        messages.add_message(request, messages.SUCCESS,
                             "Submitted Opportunity: %s, %s" % (my_opp.title, my_opp.company))
        # Redirect
        return redirect("jobber:opportunities_view_item", my_opp.id)
    else:
        contacts = get_contacts_by_user_and_role(request)
        return render(request,
                      "jobber/opportunities/add-item.html",
                      {"user": get_profile(request),
                       "stages": stages,
                       "recruiter_contacts": contacts.filter(contact_type='REC'),
                       "referral_contacts": contacts.filter(contact_type='REF')
                       })


def opportunities_delete_item(request):
    """ Deletes an Opportunity given a POST request with the opportunity id to be deleted"""
    if not request.session.get("role", False):
        return render(request,
                      "jobber/home-alt.html")

    if request.method == 'POST':
        opportunity_id = request.POST.get("id")
        my_opp = Opportunity.objects.get(pk=opportunity_id)
        if request.session['role'] != "admin" and my_opp.profile.user.username != request.session['username']:
            # TODO: Add message denying access
            return redirect("jobber:opportunities_list")
        title = my_opp.title
        company = my_opp.company
        my_opp.delete()
        # Log Action
        action = Action(
            user=get_profile(request),
            verb="deleted the opportunity %s, %s" % (my_opp.title, my_opp.company),
            target=my_opp
        )
        action.save()
        messages.add_message(request, messages.WARNING, "Deleted Opportunity: %s, %s" % (title, company))
        # Redirect
        return redirect("jobber:opportunities_list")
    else:
        stages = Stage.objects.all()
        return render(request,
                      "jobber/opportunities/add-item.html",
                      {"user": get_profile(request),
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
                profile=get_profile(request),
                name=name,
                title=title,
                company=company,
                phone_number=phone,
                email=email,
                contact_type=form_name)
            my_contact.save()
            # Log Action
            action = Action(
                user=get_profile(request),
                verb="created a new contact",
                target=my_contact
            )
            action.save()
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


# Contacts views

def contacts_list(request):
    """ List of contacts """
    if not request.session.get("role", False):
        return render(request,
                      "jobber/home-alt.html")

    contacts = get_contacts_by_user_and_role(request)
    contacts = contacts.order_by('name')
    return render(request,
                  "jobber/contacts/list.html",
                  {"user": get_profile(request),
                   "contacts": contacts}
                  )


def contacts_list_sort_ajax(request):
    """ Returns the sorted index of Contact items sent from an AJAX GET request, given a sorter name"""
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == "GET":
        sorter = request.GET.get("sorter")
        try:
            contacts = get_contacts_by_user_and_role(request)
            if sorter == "name":
                contacts = contacts.order_by("name")
            elif sorter == "company":
                contacts = contacts.order_by("company")
            contact_order = {}
            for index, opp in enumerate(contacts):
                contact_order[str(index)] = opp.id
            return JsonResponse(
                {'success': 'success', 'opportunities': contact_order},
                status=200)
        except:
            return JsonResponse(
                {'error': 'Contact not found.'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request.'}, status=400)


def contacts_view_item(request, id):
    """ Detail page of a single contact, given the contact id """
    if not request.session.get("role", False):
        return render(request,
                      "jobber/home-alt.html")
    my_contact = Contact.objects.get(pk=id)
    if request.session['role'] != "admin" and my_contact.profile.user.username != request.session['username']:
        # TODO: Add message denying access
        return redirect("jobber:contacts_list")

    return render(request,
                  "jobber/contacts/view-item.html",
                  {"user": get_profile(request),
                   "contact": my_contact})


def contacts_edit_item(request, id):
    """ Renders an existing contact's details to an editable form, saves inputs on POST request"""
    if not request.session.get("role", False):
        return render(request,
                      "jobber/home-alt.html")
    my_contact = Contact.objects.get(pk=id)
    if request.session['role'] != "admin" and my_contact.profile.user.username != request.session['username']:
        # TODO: Add message denying access
        return redirect("jobber:opportunities_list")
    if request.method == 'POST':
        my_contact = generate_contact(request=request, contact_id=id)
        action = Action(
            user=get_profile(request),
            verb="updated contact",
            target=my_contact
        )
        action.save()
        messages.add_message(request, messages.INFO, "Saved Contact: %s, %s" % (my_contact.name, my_contact.company))
        return redirect("jobber:contacts_view_item", my_contact.id)
    return render(request,
                  "jobber/contacts/add-item.html",
                  {"user": get_profile(request),
                   "contact": my_contact
                   })


def contacts_add_item(request):
    """ Renders an empty contacts form page, saves a new Contact on POST request"""
    if not request.session.get("role", False):
        return render(request,
                      "jobber/home-alt.html")

    if request.method == 'POST':
        my_contact = generate_contact(request, contact_id=None)
        # Log Action
        action = Action(
            user=get_profile(request),
            verb="created a new contact",
            target=my_contact
        )
        action.save()
        messages.add_message(request, messages.SUCCESS,
                             "Submitted Contact: %s, %s" % (my_contact.name, my_contact.title))
        # Redirect
        return redirect("jobber:contacts_view_item", my_contact.id)
    else:
        return render(request,
                      "jobber/contacts/add-item.html",
                      {"user": get_profile(request)})


def contacts_delete_item(request):
    """ Deletes a Contact given a POST request with the contact id to be deleted"""
    if not request.session.get("role", False):
        return render(request,
                      "jobber/home-alt.html")

    if request.method == 'POST':
        contact_id = request.POST.get("id")
        my_contact = Contact.objects.get(pk=contact_id)
        if request.session['role'] != "admin" and my_contact.profile.user.username != request.session['username']:
            # TODO: Add message denying access
            return redirect("jobber:contacts_list")
        name = my_contact.name
        title = my_contact.title
        my_contact.delete()
        # Log Action
        action = Action(
            user=get_profile(request),
            verb="Deleted the contact %s, %s" % (name, title),
            target=my_contact
        )
        action.save()
        messages.add_message(request, messages.WARNING, "Deleted contact: %s, %s" % (name, title))
        # Redirect
        return redirect("jobber:contacts_list")
    else:
        return render(request,
                      "jobber/contacts/add-item.html",
                      {"user": get_profile(request)})


# Events views

def events_list(request):
    """ List of events """
    if not request.session.get("role", False):
        return render(request,
                      "jobber/home-alt.html")

    events = get_events_by_user_and_role(request)
    events = events.order_by('-date')
    return render(request,
                  "jobber/events/list.html",
                  {"user": get_profile(request),
                   "events": events}
                  )


def events_list_sort_ajax(request):
    """ Returns the sorted index of Event items sent from an AJAX GET request, given a sorter name"""
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == "GET":
        sorter = request.GET.get("sorter")
        try:
            events = get_events_by_user_and_role(request)
            if sorter == "date":
                events = events.order_by("-date")
            elif sorter == "type":
                events = events.order_by("type")
            event_order = {}
            for index, opp in enumerate(events):
                event_order[str(index)] = opp.id
            return JsonResponse(
                {'success': 'success', 'opportunities': event_order},
                status=200)
        except:
            return JsonResponse(
                {'error': 'Event not found.'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request.'}, status=400)


def events_view_item(request, id):
    """ Detail page of a single event, given the event id """
    if not request.session.get("role", False):
        return render(request,
                      "jobber/home-alt.html")
    my_event = Event.objects.get(pk=id)
    if request.session['role'] != "admin" and my_event.profile.user.username != request.session['username']:
        # TODO: Add message denying access
        return redirect("jobber:events_list")

    return render(request,
                  "jobber/events/view-item.html",
                  {"user": get_profile(request),
                   "event": my_event,
                   "opportunities": my_event.opportunity_set.all()})


def events_edit_item(request, id):
    """ Renders an existing event's details to an editable form, saves inputs on POST request"""
    if not request.session.get("role", False):
        return render(request,
                      "jobber/home-alt.html")
    my_event = Event.objects.get(pk=id)
    if request.session['role'] != "admin" and my_event.profile.user.username != request.session['username']:
        # TODO: Add message denying access
        return redirect("jobber:events_list")
    if request.method == 'POST':
        my_event = generate_event(request=request, event_id=id)
        action = Action(
            user=get_profile(request),
            verb="updated event",
            target=my_event
        )
        action.save()
        messages.add_message(request, messages.INFO, "Saved Event: %s, %s" % (my_event.type, my_event.title))
        return redirect("jobber:events_view_item", my_event.id)
    return render(request,
                  "jobber/events/add-item.html",
                  {"user": get_profile(request),
                   "event": my_event,
                   "opportunities": get_opportunities_by_user_and_role(request)
                   })


def events_add_item(request):
    """ Renders an empty events form page, saves a new Event on POST request"""
    if not request.session.get("role", False):
        return render(request,
                      "jobber/home-alt.html")

    if request.method == 'POST':
        my_event = generate_event(request, event_id=None)
        # Log Action
        action = Action(
            user=get_profile(request),
            verb="created a new event",
            target=my_event
        )
        action.save()
        messages.add_message(request, messages.SUCCESS,
                             "Submitted Event: %s, %s" % (my_event.type, my_event.title))
        # Redirect
        return redirect("jobber:events_view_item", my_event.id)
    else:
        return render(request,
                      "jobber/events/add-item.html",
                      {"user": get_profile(request),
                       "opportunities": get_opportunities_by_user_and_role(request)})


def events_delete_item(request):
    """ Deletes a Event given a POST request with the event id to be deleted"""
    if not request.session.get("role", False):
        return render(request,
                      "jobber/home-alt.html")

    if request.method == 'POST':
        event_id = request.POST.get("id")
        my_event = Event.objects.get(pk=event_id)
        if request.session['role'] != "admin" and my_event.profile.user.username != request.session['username']:
            # TODO: Add message denying access
            return redirect("jobber:events_list")
        e_type = my_event.type
        title = my_event.title
        my_event.delete()
        # Log Action
        action = Action(
            user=get_profile(request),
            verb="Deleted the event %s, %s" % (e_type, title),
            target=my_event
        )
        action.save()
        messages.add_message(request, messages.WARNING, "Deleted event: %s, %s" % (e_type, title))
        # Redirect
        return redirect("jobber:events_list")
    else:
        return render(request,
                      "jobber/events/add-item.html",
                      {"user": get_profile(request)})
