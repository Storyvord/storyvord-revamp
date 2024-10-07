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

    path('api/accounts/', include('accounts.urls'),name='accounts'),
    path('api/client/', include('client.urls'),name='client'),
    path('api/crew/', include('crew.urls'),name='crew'),
    path('api/project/', include('project.urls'),name='project'),
    path('api/calendar/', include('storyvord_calendar.urls'),name='calendar'),
    path('api/tasks/', include('tasks.urls'),name='tasks'),
    path('api/callsheets/', include('callsheets.urls'),name='callsheets'),  # Add this line
    path('api/announcement/', include('announcement.urls'),name='announcement'),
    path('api/notification/', include('notification.urls'),name='notification'),
    path('api/referral/', include('referral.urls'),name='referral'),
    path('api/company/', include('company.urls'),name='company'),
    path('api/inbox/', include('inbox.urls'),name='inbox'),
    path('api/files/', include('files.urls'),name='files'),
    
    # Auth and user management
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('accounts/', include('allauth.urls')),
        
    # Schema and documentation for v1 and v2
    path('api/schema/', SpectacularAPIView.as_view(api_version='v1'), name='schema-v1'),
    path('api/schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema-v1'), name='swagger-ui-v1'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema-v1'), name='redoc-v1'),
    
    #Web view for Chat bot
    path('api/', include('ai_assistant.urls')),
    path('api/chat/', include('chat.urls')),
    
]