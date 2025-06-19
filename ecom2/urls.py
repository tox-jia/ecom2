from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('cart/', include('cart.urls')),
    path('payment/', include('payment.urls')),
    path('blog/', include('blog.urls')),
    path('time_sys/', include('time_sys.urls')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),

    # enables Google login URL
    path('accounts/', include('allauth.urls')),
]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)