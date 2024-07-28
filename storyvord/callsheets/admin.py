# # callsheets/admin.py
# from django.contrib import admin
# from .models import CallSheet

# @admin.register(CallSheet)
# class CallSheetAdmin(admin.ModelAdmin):
#     list_display = ('id', 'date', 'project_name', 'location', 'created_at')
#     list_filter = ('date', 'project_name', 'location')
#     search_fields = ('project_name', 'location')
#     ordering = ('-date',)



# callsheets/admin.py
from django.contrib import admin
from .models import CallSheet

class CallSheetAdmin(admin.ModelAdmin):
    list_display = (
        'project', 'title', 'date', 'calltime', 'breakfast', 
        'lunch',
        # 'sunrise', 'sunset',
        'created_at'  # Ensure 'created_at' exists
    )
    # Optionally, you can also include search_fields, list_filter, etc.

admin.site.register(CallSheet, CallSheetAdmin)
