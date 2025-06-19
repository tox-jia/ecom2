import cloudinary.uploader
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os


@csrf_exempt
def custom_ckeditor_upload(request):
    upload = request.FILES['upload']
    file_name = upload.name

    # Save temporarily to Cloudinary
    cloudinary_response = cloudinary.uploader.upload(upload, folder="ckeditor/")

    # Return a JSON response CKEditor expects
    return JsonResponse({
        "uploaded": 1,
        "fileName": file_name,
        "url": cloudinary_response['secure_url'],
    })