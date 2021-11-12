from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    # users views
    path('feedback/open', views.feedback_open, name="feedback_open"),
    path('feedback/<str:id>/close', views.feedback_close, name="feedback_close"),
    path('add-comment', views.comment_add_item_ajax, name="comment-add-item-ajax"),
    path('delete-comment', views.comment_delete_item_ajax, name="comment-delete-item-ajax"),
    path('edit-comment', views.comment_edit_item_ajax, name="comment-edit-item-ajax"),
]
