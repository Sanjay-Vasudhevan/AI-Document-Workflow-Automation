from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

urlpatterns = [
    # Automatic Landing Redirect: Sends root URL traffic (/) straight to /documents/
    path('', RedirectView.as_view(url='documents/', permanent=False)),

    path('admin/', admin.site.urls),
    
    # Global authentication routes (built-in views only)
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Clean routing namespaces
    path('accounts/', include('accounts.urls')),            
    path('documents/', include('documents.urls')),  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)