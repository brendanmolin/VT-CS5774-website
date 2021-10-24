from jobber.models import Stage, Event, Contact, Opportunity, User
import datetime
import pytz

# Pre-populate data

Stage(value_name='explore', name='Exploration').save()
s2 = Stage(value_name='apply', name='Preparing Application')
s2.save()
Stage(value_name='applied-waiting', name='Applied, Waiting').save()
Stage(value_name='phone', name='Preparing for Phone Interview').save()
Stage(value_name='phone-waiting', name='Phone Interviewed, Waiting').save()
s6 = Stage(value_name='interview', name='Preparing for Interview')
s6.save()
Stage(value_name='interviewed-waiting', name='Interviewed, Waiting').save()
Stage(value_name='offer', name='Considering Offer').save()
Stage(value_name='closed', name='Closed').save()
Stage(value_name='closed-accepted', name='Closed, Accepted').save()

u1 = User(username='jay', name='Jay Pritchett', reputation=120)
u1.save()
User(username='bmo', name='Admin Molin', reputation=9999).save()

e1 = Event(user=u1, date=datetime(year=2021, month=10, day=15, tzinfo=pytz.UTC), title='Interview', type='Event')
e1.save()
Event(user=u1, date=datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC), title='Apply to 5 Jobs', type='Reminder').save()

c1 = Contact(user=u1, name='John Smith', title='Recruiter', company='JP Morgan', phone_number='11001001001',
             email='john.smith@jpmorgan.com', contact_type=Contact.RECRUITER)
c1.save()
c2 = Contact(user=u1, name='Jane Doe', title='Professor', company='University of DC', phone_number='12001001001',
             email='jane.doe@udc.edu', contact_type=Contact.REFERENCE)
c2.save()
c3 = Contact(user=u1, name='Jordan Williams', title='Manager', company='Intel', phone_number='14001001001',
             email='jordan.williams@intel.com', contact_type=Contact.REFERENCE)
c3.save()
c4 = Contact(user=u1, name='Kim Lee', title='Senior Analyst', company='Google', phone_number='15001001001',
             email='kim.lee@google.com', contact_type=Contact.REFERENCE)
c4.save()
c5 = Contact(user=u1, name='Abdullah Ahmad', title='Hiring Manager', company='Comcast', phone_number='16001001001',
             email='abdullah.ahmad@google.com', contact_type=Contact.RECRUITER)
c5.save()

o1 = Opportunity(
    user=u1,
    create_date=datetime(year=2021, month=8, day=1, tzinfo=pytz.UTC),
    modified_date=datetime(year=2021, month=9, day=2, tzinfo=pytz.UTC),
    stage=s6,
    title='Data Analyst',
    company='JP Morgan',
    location='Remote',
    application_link='https://jpmorgan.com/careers/id_12345',
    recruiter_contact=c1,
    interview_location='170 VT Lane, Blacksburg VA 21111',
    interview_date=datetime(year=2021, month=10, day=16, tzinfo=pytz.UTC),
    next_step='Prepare for Interview')
o1.save()
o1.referral_contacts.add(c2, c3)
o1.events.add(e1)

o2 = Opportunity(
    user=u1,
    create_date=datetime(year=2021, month=8, day=11, tzinfo=pytz.UTC),
    modified_date=datetime(year=2021, month=10, day=13, tzinfo=pytz.UTC),
    stage=s2,
    title='Software Developer',
    company='Comcast',
    location='Philadelphia, PA',
    application_link='https://comcast.com/careers/id_12345',
    interview_location='',
    next_step='Apply')
o2.save()

""" Delete data from tables, mysql
DELETE FROM public.jobber_opportunity_events;
DELETE FROM public.jobber_opportunity;
DELETE FROM public.jobber_opportunity_referral_contacts;
DELETE FROM public.jobber_contact;
DELETE FROM public.jobber_stage;
"""