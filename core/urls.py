"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from core import settings
from django.conf.urls.static import static
from renderer import views  # Import views from renderer

swagger_urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urlpatterns = [
    path('', views.home, name='home'),           # Homepage with banner
    path('about/', views.about, name='about'),   # About Us page
    path('faq/', views.faq, name='faq'),         # FAQ page
    path('noticeboard/', views.noticeboard, name='noticeboard'),  # NoticeBoard page

    path('admin/', admin.site.urls),
    path('user/', include('apps.user.urls.urls_v1')),
    path('user_profile/', include('apps.user_profile.urls.urls_v1')),
    path('authentication/', include('apps.authentication.urls.urls_v1')),
    path('dashboard/', include('apps.dashboard.urls.urls_v1')),
] + swagger_urlpatterns

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
