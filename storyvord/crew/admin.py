from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(CrewProfile)
admin.site.register(CrewCredits)
admin.site.register(CrewEducation)
admin.site.register(EndorsementfromPeers)
admin.site.register(SocialLinks)
admin.site.register(CrewEvent)
admin.site.register(CrewPortfolio)