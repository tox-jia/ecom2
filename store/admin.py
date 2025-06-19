from django.contrib import admin
from .models import Category, Product, Order, Profile, Membership
from django.contrib.auth.models import User

admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Profile)
admin.site.register(Membership)


# mix Profile info and User info
class ProfileInline(admin.StackedInline):
    model = Profile

# extern User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInline]


# unregister the old way
admin.site.unregister(User)

# Re-register the new way
admin.site.register(User, UserAdmin)



from django import forms

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    class Media:
        js = [
            'https://cdnjs.cloudflare.com/ajax/libs/cropperjs/1.5.13/cropper.min.js',
            '/static/js/image_cropper.js',  # your custom JS
        ]
        css = {
            'all': [
                'https://cdnjs.cloudflare.com/ajax/libs/cropperjs/1.5.13/cropper.min.css',
            ]
        }

class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
admin.site.register(Product, ProductAdmin)

