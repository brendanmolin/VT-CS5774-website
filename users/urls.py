from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    # users views
    path('register', views.register, name="register"),
]
