"""
URL configuration for retrospectives project.
"""
import os
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Only serve frontend static files and catch-all route when NOT in Docker
# In Docker, the frontend is served by Vite on port 3000
if not os.path.exists('/app/frontend/dist'):
    # Serve frontend static files
    urlpatterns += static('/', document_root='/app/frontend/dist')
    
    # Catch-all route for frontend SPA
    urlpatterns += [
        re_path(r'^.*$', TemplateView.as_view(template_name='index.html'), name='frontend'),
    ] 