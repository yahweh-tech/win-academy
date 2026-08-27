"""
URL configuration for WIN PROFESSIONAL ACADEMY project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from academy.views import health_check_view

# Custom Admin Site Header & Title
admin.site.site_header = "WIN PROFESSIONAL ACADEMY Administration"
admin.site.site_title = "Win Academy Admin Portal"
admin.site.index_title = "Academy Management & Admissions Dashboard"

urlpatterns = [
    # Top-level direct health check endpoint for Render / Docker
    path('health/', health_check_view, name='health_check'),
    
    # Django Admin
    path('admin/', admin.site.urls),
    
    # Academy main application
    path('', include('academy.urls', namespace='academy')),
]

# Serve media files locally during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'academy.views.custom_404_view'
handler500 = 'academy.views.custom_500_view'
