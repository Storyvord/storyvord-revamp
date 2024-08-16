from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(ClientProfile)
admin.site.register(ClientCompanyProfile)
admin.site.register(ClientCompanyCalendar)
admin.site.register(ClientCompanyEvent)
