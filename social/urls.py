from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    # users views
    path('feedback/open', views.feedback_open, name="feedback_open"),
    path('feedback/<str:id>/close', views.feedback_close, name="feedback_close"),
]
