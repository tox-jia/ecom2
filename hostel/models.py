from email.policy import default

from django.db import models
import datetime
from django.contrib.auth.models import User

# whever a user signs up, it signs up an automatic django user system,
# it creates a user model, we also want to automatically create a profile for them, so
# this will allow us to create a profile using the signal.
from django.db.models.signals import post_save

from cloudinary.models import CloudinaryField
from django_ckeditor_5.fields import CKEditor5Field


# check-in guest
class Guest(models.Model):
    date_modified = models.DateTimeField(auto_now=True)
    givenname = models.CharField(max_length=30, blank=True)
    surname = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=30, blank=True)
    platform = models.CharField(max_length=30, blank=True)
    passport = CloudinaryField('image', blank=False, null=False)

    # for the admin section
    def __str__(self):
        return self.givenname
