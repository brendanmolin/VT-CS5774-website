from django.db import models
from datetime import datetime


# Create your models here.


class Contact:
    def __init__(self, id, name, title, company, phone_number, email):
        self.id = id
        self.name = name
        self.title = title
        self.company = company
        self.phone_number = phone_number
        self.email = email


class Opportunity:
    def __init__(self, id, create_date, modified_date, stage, title, company, location, recruiter_contacts,
                 application_link, application, referral_contacts, interview_location, interview_date, events,
                 next_step):
        self.id = id
        self.create_date = create_date
        self.modified_date = modified_date
        self.stage = stage
        self.title = title
        self.company = company
        self.location = location
        self.recruiter_contacts = recruiter_contacts
        self.application_link = application_link
        self.application = application
        self.referral_contacts = referral_contacts
        self.interview_location = interview_location
        self.interview_date = interview_date
        self.events = events
        self.next_step = next_step


class Stage:
    def __init__(self, id, value_name, name):
        self.id = id
        self.value_name = value_name
        self.name = name


class Event:
    def __init__(self, id, date, title, type):
        self.id = id
        self.date = date
        self.title = title
        self.type = type


class Resume:
    def __init__(self, id, contact, experiences, education, skills):
        self.id = id
        self.contact = contact
        self.experiences = experiences
        self.education = education
        self.skills = skills


class CoverLetter:
    def __init__(self, id, text):
        self.id = id
        self.text = text


class Application:
    def __init__(self, id, cover_letter, resume):
        self.id = id
        self.cover_letter = cover_letter
        self.resume = resume


class Feedback:
    def __init__(self, id, application_id, date, by_user_id):
        self.id = id
        self.application_id = application_id
        self.date = date
        self.by_user_id = by_user_id


class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Article:
    def __init__(self, id, date_posted, title, subtitle, text, author):
        self.id = id
        self.date_posted = date_posted
        self.title = title
        self.subtitle = subtitle
        self.text = text
        self.author = author


# Create data
stages = []
contacts = []
cover_letters = []
resumes = []
application = []
events = []
opportunities = []
authors = []
articles = []

stages.append(Stage(1, "explore", "Exploration"))
stages.append(Stage(2, "apply", "Preparing Application"))
stages.append(Stage(3, "applied-waiting", "Applied, Waiting"))
stages.append(Stage(4, "phone", "Preparing for Phone Interview"))
stages.append(Stage(5, "phone-waiting", "Phone Interviewed, Waiting"))
stages.append(Stage(6, "interview", "Preparing for Interview"))
stages.append(Stage(7, "interviewed-waiting", "Interviewed, Waiting"))
stages.append(Stage(8, "offer", "Considering Offer"))
stages.append(Stage(9, "closed", "Closed"))
stages.append(Stage(10, "closed-accepted", "Closed, Accepted"))

contacts.append(Contact(1, "John Smith", "Recruiter", "JP Morgan", "100-100-1001", "john.smith@jpmorgan.com"))
contacts.append(Contact(2, "Jane Doe", "Professor", "University of DC", "200-100-1001", "jane.doe@udc.edu"))
contacts.append(Contact(3, "Jordan Williams", "Manager", "Intel", "400-100-1001", "jordan.williams@intel.com"))

cover_letters.append(
    CoverLetter(id=1, text="I am a very experienced data analyst and I would like to work at your company"))

resumes.append(Resume(id=1, contact="Brendan Molin, 1234 Happy Lane, 999-9999-9999",
                      experiences=["Data Analyst, Comlinkdata.  Did a lot of analytics."],
                      education="Northeastern University", skills=["Clustering, Statistics"]))

application.append(Application(id=1, cover_letter=cover_letters[0], resume=resumes[0]))

events.append(Event(id=1, date=datetime.now(), title="Interview", type="Event"))
events.append(Event(id=2, date=datetime.now(), title="Apply to 3 Jobs", type="Reminder"))

opportunities.append(Opportunity(
    id=1,
    modified_date=datetime.now(),
    create_date=datetime.now(),
    stage=stages[5],
    title="Data Analyst",
    company="JP Morgan",
    location="Remote",
    recruiter_contacts=[contacts[0]],
    application_link="https://jpmorgan.com/careers/id_12345",
    application=application,
    referral_contacts=[contacts[1], contacts[2]],
    events=[events[0]],
    interview_location="170 VT Lane, Blacksburg VA 21111",
    interview_date=datetime.now(),
    next_step="Prepare for Interview"
))

opportunities.append(Opportunity(
    id=2,
    modified_date=datetime.now(),
    create_date=datetime.now(),
    stage=stages[3],
    title="Software Developer",
    company="Comcast",
    location="Philadelphia, PA",
    recruiter_contacts=[],
    application_link="https://comcast.com/careers/id_12345",
    application=None,
    referral_contacts=[contacts[1]],
    events=None,
    interview_location=None,
    interview_date=None,
    next_step="Apply"
))

authors.append(Author(
    id=1,
    name="Jordan Joseph"
))

articles.append(Article(
    id=1,
    date_posted=datetime.now(),
    title="Resume Tips: How Many Pages Is Right For You?",
    subtitle="When building your resume, your goal is to put as much relevant experience as possible. Sometimes though you need more than one page to do so, but conventional wisdom is that resumes should fit in one page..",
    text="When building your resume, your goal is to put as much relevant experience as possible. Sometimes though you need more than one page to do so, but conventional wisdom is that resumes should fit in one page.  But in the end, your goal is to put forth your best qualifications.  One page is a minimum, not a limit.",
    author=authors[0]
))

regular_user = {"username": "jay", "password": "regular"}
admin_user = {"username": "bmo", "password": "mlogin"}
