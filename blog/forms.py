from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import BlogPost

class BlogPostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditor5Widget(config_name='default'))

    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'id': 'editor'})
        }