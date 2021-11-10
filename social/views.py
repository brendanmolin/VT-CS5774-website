from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect


# Create your views here.
from actions.models import Action


def feedback_open(request):
    """ Opens a new feedback object on an opportunity and closes previous ones, given an opportunity id """
    if not request.session.get("role", False):
        return render(request,
                      "jobber/home-alt.html")
    print(request.method)
    if request.method == 'POST':
        opportunity_id = request.POST.get('opp-id')
        # Log Action
        """
        action = Action(
            user=get_profile(request),
            verb="updated opportunity",
            target=my_opp
        )
        action.save()
        """

        messages.add_message(request, messages.INFO, "requested feedback for application")
        return redirect("jobber:opportunities_view_item", id=opportunity_id)
    return redirect("jobber:opportunities_index")


def feedback_close(request, id):
    """ Closes the active feedback object on an opportunity, given a feedback id """
    if not request.session.get("role", False):
        return render(request,
                      "jobber/home-alt.html")
    if request.method == 'POST':
        opportunity_id = request.POST.get('opp-id')
        # Log Action
        """
        action = Action(
            user=get_profile(request),
            verb="updated opportunity",
            target=my_opp
        )
        action.save()
        """

        messages.add_message(request, messages.INFO, "Closed feedback request for application")
        return redirect("jobber:opportunities_view_item", id=opportunity_id)
    return redirect("jobber:opportunities_index")


def comment_add_item_ajax(request):
    """ Adds a Comment to the active feedback given a feedback id sent from an AJAX request """
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == "POST":
        try:
            return JsonResponse(
                {'success': 'success'},  # send back a comment id
                status=200)
        except:
            return JsonResponse(
                {'error': 'Contact not found.'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request.'}, status=400)


def comment_edit_item_ajax(request):
    """ Edits a given Comment comment given a comment id sent from an AJAX request """
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == "POST":
        try:
            return JsonResponse(
                {'success': 'success'},
                status=200)
        except:
            return JsonResponse(
                {'error': 'Contact not found.'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request.'}, status=400)


def comment_delete_item_ajax(request):
    """ Deletes a Comment given a comment id sent from an AJAX request """
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == "POST":
        try:
            return JsonResponse(
                {'success': 'success'},
                status=200)
        except:
            return JsonResponse(
                {'error': 'Contact not found.'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request.'}, status=400)


def comment_vote_ajax(request):
    """ Increments a Comment vote to a comment given a comment id sent from an AJAX request """
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == "POST":
        try:
            return JsonResponse(
                {'success': 'success'},
                status=200)
        except:
            return JsonResponse(
                {'error': 'Contact not found.'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request.'}, status=400)
