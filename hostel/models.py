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
    selfie = CloudinaryField('image', blank=False, null=False)
    terms_answers = models.JSONField(default=dict, blank=True)
    room = models.ForeignKey(
        "RoomState",
        on_delete=models.SET_NULL,  # keeps guest even if room is deleted
        null=True,
        blank=True,
        related_name="guests"
    )
    start_day = models.PositiveIntegerField(null=True, blank=True)
    end_day = models.PositiveIntegerField(null=True, blank=True)

    # for the admin section
    def __str__(self):
        return self.givenname




class Term(models.Model):
    ANSWER_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    question_en = models.TextField()
    question_zh = models.TextField(blank=True)
    question_th = models.TextField(blank=True)

    warning_message_en = models.TextField(blank=True)
    warning_message_zh = models.TextField(blank=True)
    warning_message_th = models.TextField(blank=True)

    correct_answer = models.CharField(max_length=10, choices=ANSWER_CHOICES)

    def get_question(self, lang):
        if lang == 'zh':
            return self.question_zh or self.question_en
        elif lang == 'th':
            return self.question_th or self.question_en
        return self.question_en

    # ✅ ADD THIS HERE (inside the class)
    def get_warning(self, lang):
        if lang == 'zh':
            return self.warning_message_zh or self.warning_message_en
        elif lang == 'th':
            return self.warning_message_th or self.warning_message_en
        return self.warning_message_en

    def __str__(self):
        return self.question_en

# Room
class RoomState(models.Model):
    name = models.CharField(max_length=30, blank=False)
    out = models.BooleanField(default=False)
    key = models.BooleanField(default=False)
    is_clean = models.BooleanField(default=False)
    is_extend = models.BooleanField(default=False)

    # for the admin section
    def __str__(self):
        return self.name


# Allergy
class Allergy(models.Model):
    item_en = models.CharField(max_length=30, blank=False)
    item_cn = models.CharField(max_length=30, blank=False)
    item_th = models.CharField(max_length=30, blank=False)

    # for the admin section
    def __str__(self):
        return self.item_en

# Restaurant Order
class ResOrder(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    allergy = models.CharField(max_length=200, blank=False)
    order = models.CharField(max_length=200, blank=False)

    # for the admin section
    def __str__(self):
        return self.id


# Restaurant Food
class Food(models.Model):
    foodType = models.ForeignKey(
        "FoodType",
        on_delete=models.SET_NULL,  # keeps guest even if room is deleted
        null=True,
        blank=True,
        related_name="foodType"
    )
    name = models.CharField(max_length=200, blank=False)

    # for the admin section
    def __str__(self):
        return self.name


# Restaurant Food
class FoodType(models.Model):
    name = models.CharField(max_length=200, blank=False)

    # for the admin section
    def __str__(self):
        return self.name


# Monthly Job
class MonthlyJob(models.Model):
    name = models.CharField(max_length=200, blank=False)

    # for the admin section
    def __str__(self):
        return self.name

class MonthlyJobRecord(models.Model):
    job = models.ForeignKey(
        "MonthlyJob",
        on_delete=models.SET_NULL,  # keeps guest even if room is deleted
        null=True,
        blank=True,
        related_name="records"
    )
    year = models.IntegerField()
    month = models.IntegerField()
    is_done = models.BooleanField(default=False)
    payment = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # for the admin section
    def __str__(self):
        return f"{self.job} - {self.year}-{self.month}"


class MonthlyJobImage(models.Model):
    record = models.ForeignKey(
        "MonthlyJobRecord",
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = CloudinaryField('image')