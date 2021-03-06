from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, default="registered")
    reputation = models.IntegerField(default=0)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)

    def get_absolute_url(self):
        return reverse("users:profile", args=[self.user.username])



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_details(sender, instance, **kwargs):
    instance.profile.save()