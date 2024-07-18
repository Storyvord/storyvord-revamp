# callsheets/admin.py
from django.contrib import admin
from .models import CallSheet

@admin.register(CallSheet)
class CallSheetAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'project_name', 'location', 'created_at')
    list_filter = ('date', 'project_name', 'location')
    search_fields = ('project_name', 'location')
    ordering = ('-date',)