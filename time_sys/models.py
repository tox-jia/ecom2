from readline import set_completer
from django.contrib.auth.models import User
from django.db import models
import datetime
import pytz

class TimeRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    end = models.DateTimeField()
    duration = models.IntegerField()
    tag = models.CharField(max_length=255)
    type = models.CharField(max_length=255)

    @property
    def formatted_duration(self):
        seconds = self.duration
        minutes = self.duration // 60
        seconds = seconds % 60
        if minutes < 60:
            return f"{minutes}M"
        hours = minutes // 60
        minutes = minutes % 60
        return f"{hours}h {minutes}m {seconds}s"

    def __str__(self):
        return f'{self.user} - {self.tag} - {self.type}'





class TimeTag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.CharField(max_length=255)
    type = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.user} - {self.tag}'


# class TimeReport(models.Model):
#     year_date = models.CharField(max_length=255, blank=True, null=True)
#     type_sl = models.CharField(max_length=255)
#     percent_sl = models.CharField(max_length=255)
#     type_pr = models.CharField(max_length=255)
#     percent_pr = models.CharField(max_length=255)
#     type_un = models.CharField(max_length=255)
#     percent_un = models.CharField(max_length=255)
#     detail = models.CharField(max_length=255)
#
#     def __str__(self):
#         return f'Report {self.year_date}'




class TimeReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year_month = models.CharField(max_length=7)  # e.g. "2025-06"
    total_duration = models.IntegerField(default=0)
    type_data = models.JSONField(default=dict)
    tag_data = models.JSONField(default=dict)

    def __str__(self):
        return f'{self.user} - {self.year_month}'

    class Meta:
        unique_together = ('user', 'year_month')