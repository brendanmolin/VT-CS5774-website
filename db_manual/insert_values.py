from django.db import models
from jobber.models import Stage, Event, Contact, Opportunity
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

e1 = Event(date=datetime(year=2021, month=10, day=15, tzinfo=pytz.UTC), title='Interview', type='Event')
e1.save()
Event(date=datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC), title='Apply to 5 Jobs', type='Reminder').save()

c1 = Contact(name='John Smith', title='Recruiter', company='JP Morgan', phone_number='11001001001',
             email='john.smith@jpmorgan.com')
c1.save()
c2 = Contact(name='Jane Doe', title='Professor', company='University of DC', phone_number='12001001001',
             email='jane.doe@udc.edu')
c2.save()
c3 = Contact(name='Jordan Williams', title='Manager', company='Intel', phone_number='14001001001',
             email='jordan.williams@intel.com')
c3.save()

o1 = Opportunity(
    create_date=datetime(year=2021, month=8, day=1, tzinfo=pytz.UTC),
    modified_date=datetime(year=2021, month=9, day=2, tzinfo=pytz.UTC),
    stage=s6,
    title='Data Analyst',
    company='JP Morgan',
    location='Remote',
    application_link='https://jpmorgan.com/careers/id_12345',
    interview_location='170 VT Lane, Blacksburg VA 21111',
    interview_date=datetime(year=2021, month=10, day=16, tzinfo=pytz.UTC),
    next_step='Prepare for Interview')
o1.save()
o1.recruiter_contacts.add(c1)
o1.referral_contacts.add(c2, c3)
o1.events.add(e1)

o2 = Opportunity(
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

"""
INSERT INTO public.jobber_contact(id, name, title, company, phone_number, email)
VALUES (DEFAULT, 'John Smith', 'Recruiter', 'JP Morgan', '11001001001', 'john.smith@jpmorgan.com'),
       (DEFAULT, 'Jane Doe', 'Professor', 'University of DC', '12001001001', 'jane.doe@udc.edu'),
       (DEFAULT, 'Jordan Williams', 'Manager', 'Intel', '14001001001', 'jordan.williams@intel.com');

INSERT INTO public.jobber_coverletter(id, text)
VALUES (DEFAULT, 'I am a very experienced data analyst and I would like to work at your company');

INSERT INTO public.jobber_resume(id, contact, experiences, education, skills)
VALUES (DEFAULT, 'Brendan Molin, 1234 Happy Lane, 999-9999-9999',
        'Data Analyst, Comlinkdata.  Did a lot of analytics.',
        'Northeastern University', 'Clustering, Statistics');

INSERT INTO public.jobber_application(id, cover_letter_id, resume_id)
VALUES (DEFAULT, 1, 1);

INSERT INTO public.jobber_event(id, date, title, type)
VALUES (DEFAULT, '2021-10-15', 'Interview', 'Event'),
       (DEFAULT, '2022-01-01', 'Apply to 5 Jobs', 'Reminder');

INSERT INTO public.jobber_opportunity(id, create_date, modified_date, stage, title, company, location, application_link,
                                      interview_location, interview_date, next_step, application_id)
VALUES (DEFAULT,
        '2021-08-01',
        '2021-09-02',
        6,
        'Data Analyst',
        'JP Morgan',
        'Remote',
        'https://jpmorgan.com/careers/id_12345',
        '170 VT Lane, Blacksburg VA 21111',
        '2021-10-15',
        'Prepare for Interview',
        1),
       (DEFAULT,
        '2021-08-11',
        '2021-08-13',
        4,
        'Software Developer',
        'Comcast',
        'Philadelphia, PA',
        'https://comcast.com/careers/id_12345',
        '',
        Null,
        'Apply',
        NULL);
INSERT INTO public.jobber_opportunity_events(id, opportunity_id, event_id)
VALUES (DEFAULT, 2, 1);
INSERT INTO public.jobber_opportunity_recruiter_contacts(id, opportunity_id, contact_id)
VALUES (DEFAULT, 1, 1);
INSERT INTO public.jobber_opportunity_referral_contacts(id, opportunity_id, contact_id)
VALUES (DEFAULT, 1, 2),
       (DEFAULT, 1, 3);

INSERT INTO public.jobber_author(id, name)
VALUES (DEFAULT,
        'Jordan Joseph');

INSERT INTO public.jobber_article(id, date_posted, title, subtitle, text, author_id)
VALUES (DEFAULT,
        '2021-06-28',
        'Resume Tips: How Many Pages Is Right For You?',
        'When building your resume, your goal is to put as much relevant experience as possible. Sometimes though you need more than one page to do so, but conventional wisdom is that resumes should fit in one page..',
        'When building your resume, your goal is to put as much relevant experience as possible. Sometimes though you need more than one page to do so, but conventional wisdom is that resumes should fit in one page.  But in the end, your goal is to put forth your best qualifications.  One page is a minimum, not a limit.',
        1);
"""
