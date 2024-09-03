"""
URL configuration for storyvord project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from rest_framework import routers, permissions
#from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


# schema_view = get_schema_view(
#     openapi.Info(
#         title="Storyvord APIs",
#         default_version='v1',),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/client/', include('client.urls')),
    path('api/crew/', include('crew.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/project/', include('project.urls')),
    path('api/calendar/', include('storyvord_calendar.urls')),
    path('api/tasks/', include('tasks.urls')),
    path('api/callsheets/', include('callsheets.urls')),  # Add this line
    path('api/announcement/', include('announcement.urls')),
    path('api/notification/', include('notification.urls')),
    path('api/referral/', include('referral.urls')),
    path('api/company/', include('company.urls')),
    path('api/inbox/', include('inbox.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    
    # Endpoint for the API schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Endpoints for Swagger and Redoc UIs
    path('api/schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('api/files/', include('files.urls')),
]
