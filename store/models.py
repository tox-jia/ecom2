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


# create profile
class Profile(models.Model):
    # if the user is deleted, the profile page is deleted as well, it's a one-one connection
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    # people type in their phone number in all kinds of ways, so CharField.
    # people can choose not to type in the phone number, so blank can be True
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    # can be an alternative address
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    old_cart = models.CharField(max_length=200, blank=True, null=True)

    # NEW field for timezone
    timezone = models.CharField(max_length=50, default="Etc/GMT-0")

    # for the admin section
    def __str__(self):
        return self.user.username


# create a user profile whenever register by default
def create_profile(sender, instance, created, **kwargs):
    # 'instance' is whenever the user fills the form in registeration page
    if created:
        user_profile = Profile(user=instance)
        # 'instance' is with 'one to one' connection with Profile
        user_profile.save()

# automate the profile thing
post_save.connect(create_profile, sender=User)


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    # this is to show the name to the admin interface
    class Meta:
        verbose_name_plural = 'categories'


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    # if price is 9999.99, so the number of digit is 6
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    # blank=True, means no necessary to have a description
    # image = models.ImageField(upload_to='uploads/product/')
    image = CloudinaryField('image')
    # we need to install PILLOW (python image library), pip3 install Pillow
    # add Sale stuff
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    # membership = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Membership(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    description = CKEditor5Field('Content', config_name='default')
    image = CloudinaryField('image')
    is_active = models.BooleanField(default=False)
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)

    def __str__(self):
        return self.name


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='', blank=True, null=True)
    #cuz some users order ebook, no need to ship
    phone = models.CharField(max_length=20, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)
    #shipped or not

    def __str__(self):
        return self.product

