INSERT INTO public.jobber_stage(id, value_name, name)
VALUES (DEFAULT, 'explore', 'Exploration'),
       (DEFAULT, 'apply', 'Preparing Application'),
       (DEFAULT, 'applied-waiting', 'Applied, Waiting'),
       (DEFAULT, 'phone', 'Preparing for Phone Interview'),
       (DEFAULT, 'phone-waiting', 'Phone Interviewed, Waiting'),
       (DEFAULT, 'interview', 'Preparing for Interview'),
       (DEFAULT, 'interviewed-waiting', 'Interviewed, Waiting'),
       (DEFAULT, 'offer', 'Considering Offer'),
       (DEFAULT, 'closed', 'Closed'),
       (DEFAULT, 'closed-accepted', 'Closed, Accepted');

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