from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from marketplace.views import index, contact

app_name = 'marketplace'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('contact/', contact, name="contact")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)