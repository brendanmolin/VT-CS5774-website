from datetime import datetime
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.humanize.templatetags.humanize import naturaltime
from actions.models import Action
from jobber.models import Opportunity, Application
from users.models import Profile
from social.models import Feedback, Comment


# Helpers
def get_profile(request):
    return Profile.objects.get(user__username=request.session['username'])


# Create your views here.
def feedback_open(request):
    """ Opens a new feedback object on an opportunity and closes previous ones, given an opportunity id """
    if not request.session.get("role", False):
        return render(request,
                      "jobber/home-alt.html")
    if request.method == 'POST':
        opportunity_id = request.POST.get('opp-id')
        # Add Feedback
        my_feedback = Feedback(
            application=Opportunity.objects.get(pk=opportunity_id).application,
            message="Please give me feedback on my application",
            status=Feedback.OPEN
        )
        my_feedback.save()
        # Log Action
        action = Action(
            user=get_profile(request),
            verb="Requested feedback for application on opportunity",
            target=Opportunity.objects.get(pk=opportunity_id)
        )
        action.save()

        messages.add_message(request, messages.INFO, "Requested feedback")
        return redirect("jobber:opportunities_view_item", id=opportunity_id)
    return redirect("jobber:opportunities_index")


def feedback_close(request, id):
    """ Closes the active feedback object on an opportunity, given a feedback id """
    if not request.session.get("role", False):
        return render(request,
                      "jobber/home-alt.html")
    if request.method == 'POST':
        opportunity_id = request.POST.get('opp-id')
        # Close feedback
        my_feedback = Feedback.objects.get(pk=id)
        my_feedback.status = Feedback.CLOSED
        my_feedback.save()
        # Log Action
        action = Action(
            user=get_profile(request),
            verb="Closed feedback for application on opportunity",
            target=Opportunity.objects.get(pk=opportunity_id)
        )
        action.save()

        messages.add_message(request, messages.INFO, "Closed feedback request for application")
        return redirect("jobber:opportunities_view_item", id=opportunity_id)
    return redirect("jobber:opportunities_index")


def comment_add_item_ajax(request):
    """ Adds a Comment to the active feedback given a feedback id sent from an AJAX request """
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == "POST":
        try:
            comment = request.POST.get('comment')
            profile_id = request.POST.get('profile_id')
            feedback_id = request.POST.get('feedback_id')
            my_comment = Comment(
                profile=Profile.objects.get(pk=profile_id),
                feedback=Feedback.objects.get(pk=feedback_id),
                comment=comment
            )
            my_comment.save()
            comment_id = my_comment.id
            comment_date = my_comment.date_modified
            title = my_comment.feedback.application.opportunity.title
            company = my_comment.feedback.application.opportunity.company
            # Log Action
            action = Action(
                user=get_profile(request),
                verb="Added a comment on opportunity %s, %s" % (title, company),
                target=my_comment.feedback.application.opportunity
            )
            action.save()
            return JsonResponse(
                {'success': 'success',
                 'comment_id': comment_id,
                 'comment_date': naturaltime(comment_date)},
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
        #try:
            comment = request.POST.get('comment')
            comment_id = request.POST.get('comment_id')
            my_comment = Comment.objects.get(pk=comment_id)
            my_comment.comment = comment
            my_comment.date_modified = datetime.now()
            my_comment.save()
            title = my_comment.feedback.application.opportunity.title
            company = my_comment.feedback.application.opportunity.company
            # Log Action
            action = Action(
                user=get_profile(request),
                verb="Edited the comment on opportunity %s, %s" % (title, company),
                target=my_comment.feedback.application.opportunity
            )
            action.save()
            return JsonResponse(
                {'success': 'success',
                 'comment_date': naturaltime(my_comment.date_modified)},  # send back a comment id
                status=200)
        #except:
            return JsonResponse(
                {'error': 'Contact not found.'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request.'}, status=400)


def comment_delete_item_ajax(request):
    """ Deletes a Comment given a comment id sent from an AJAX request """
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == "POST":
        try:
            comment_id = request.POST.get('comment_id')
            my_comment = Comment.objects.get(pk=comment_id)
            title = my_comment.feedback.application.opportunity.title
            company = my_comment.feedback.application.opportunity.company
            my_comment.delete()
            # Log Action
            action = Action(
                user=get_profile(request),
                verb="Deleted the comment on opportunity %s, %s" % (title, company),
                target=my_comment.feedback.application.opportunity
            )
            action.save()
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
