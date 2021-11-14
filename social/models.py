from django.db import models
from jobber.models import Application
from users.models import Profile


# Create your models here.

class Feedback(models.Model):
    OPEN = 'OPEN'
    COMPLETE = 'COMPLETE'
    CLOSED = 'CLOSED'
    STATUS_CHOICES = [
        (OPEN, 'Open'),
        (COMPLETE, 'Complete'),
        (CLOSED, 'Closed')
    ]
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=9,
        choices=STATUS_CHOICES,
        default=OPEN
    )


class Comment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)
    comment = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)
    votes = models.IntegerField(default=0)
