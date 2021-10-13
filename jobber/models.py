from django.db import models
from datetime import datetime


# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=11)
    email = models.CharField(max_length=200)


class Opportunity(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    stage = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200, )
    recruiter_contacts = models.ManyToManyField("Contact", related_name="recruiter_contacts")
    application_link = models.CharField(max_length=200)
    application = models.ForeignKey('Application', on_delete=models.CASCADE, null=True, blank=True)
    referral_contacts = models.ManyToManyField("Contact", related_name="referral_contacts")
    interview_location = models.CharField(max_length=200)
    interview_date = models.DateTimeField(null=True, blank=True)
    events = models.ManyToManyField("Event")
    next_step = models.CharField(max_length=200)


class Stage(models.Model):
    value_name = models.CharField(max_length=200)
    name = models.CharField(max_length=200)


class Event(models.Model):
    date = models.DateTimeField()
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=200)


class Resume(models.Model):
    contact = models.CharField(max_length=200)
    experiences = models.TextField()
    education = models.TextField()
    skills = models.TextField()


class CoverLetter(models.Model):
    text = models.CharField(max_length=200)


class Application(models.Model):
    cover_letter = models.ForeignKey('CoverLetter', on_delete=models.CASCADE, null=True, blank=True)
    resume = models.ForeignKey('Resume', on_delete=models.CASCADE)


class Feedback(models.Model):
    application = models.ForeignKey('Application', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class Author(models.Model):
    name = models.CharField(max_length=200)


class Article(models.Model):
    date_posted = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=400)
    text = models.TextField()
    author = models.ForeignKey('Author', on_delete=models.CASCADE, null=True, blank=True)

regular_user = {"username": "jay", "password": "regular"}
admin_user = {"username": "bmo", "password": "mlogin"}
