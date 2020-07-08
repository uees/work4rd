"""work4rd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.static import serve

from work4rd.api_router import router

admin.AdminSite.site_title = "Work4RD"
admin.AdminSite.site_header = "Work4RD Admin"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include('apps.account.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns.extend([
        path('__debug__/', include(debug_toolbar.urls)),
        path('media/<path>', serve, {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        path('static/<path>', serve, {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
    ])
