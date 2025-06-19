from django.contrib import admin
from .models import BlogPost, BlogCategory

admin.site.register(BlogCategory)

from django import forms

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
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

class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostForm
admin.site.register(BlogPost, BlogPostAdmin)