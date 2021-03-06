from django.db import models
from users.models import Profile
from django.urls import reverse
from datetime import datetime
import pytz


# Create your models here.
class Contact(models.Model):
    REFERENCE = 'REF'
    RECRUITER = 'REC'
    CONTACT_TYPE_CHOICES = [
        (REFERENCE, 'Reference'),
        (RECRUITER, 'Recruiter'),
    ]
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=12)
    email = models.EmailField(max_length=200)
    contact_type = models.CharField(
        max_length=9,
        choices=CONTACT_TYPE_CHOICES,
        default=REFERENCE
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("jobber:contacts_view_item", args=[self.id])


class Opportunity(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    stage = models.ForeignKey("Stage", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200, )
    recruiter_contact = models.ForeignKey("Contact", related_name="recruiter_contact", on_delete=models.CASCADE,
                                          null=True)
    application = models.OneToOneField('Application', on_delete=models.CASCADE, null=True, blank=True)
    referral_contacts = models.ManyToManyField("Contact", related_name="referral_contacts")
    events = models.ManyToManyField("Event")
    next_step = models.CharField(max_length=200)

    def __str__(self):
        return "%s, %s" % (self.title, self.company)

    def get_absolute_url(self):
        return reverse("jobber:opportunities_view_item", args=[self.id])


class Stage(models.Model):
    value_name = models.CharField(max_length=200)
    name = models.CharField(max_length=200)


class Event(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateTimeField()
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=200)

    def __str__(self):
        return "%s, %s" % (self.type, self.title)

    def get_absolute_url(self):
        return reverse("jobber:events_view_item", args=[self.id])


class Resume(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    text = models.TextField(null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % (self.name)

    def get_absolute_url(self):
        return reverse("jobber:resumes_view_item", args=[self.id])


class CoverLetter(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    text = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % (self.name)

    def get_absolute_url(self):
        return reverse("jobber:coverletters_view_item", args=[self.id])


class Application(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    application_link = models.URLField(max_length=200, null=True, blank=True)
    cover_letter = models.ForeignKey('CoverLetter', on_delete=models.CASCADE, null=True)
    resume = models.ForeignKey('Resume', on_delete=models.CASCADE, null=True)


class Author(models.Model):
    name = models.CharField(max_length=200)


class Article(models.Model):
    date_posted = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=400)
    text = models.TextField()
    author = models.ForeignKey('Author', on_delete=models.CASCADE, null=True, blank=True)
