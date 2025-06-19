from django.db import models
import datetime
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
from cloudinary.models import CloudinaryField


class BlogCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    # this is to show the name to the admin interface
    class Meta:
        verbose_name_plural = 'blog_categories'


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = CKEditor5Field('Content', config_name='default')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    image = CloudinaryField('image', null=True, blank=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.PROTECT, default=1)

    def __str__(self):
        return self.title



