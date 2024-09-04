from django.contrib import admin
from .models import *

@admin.register(CallSheet)
class CallSheetAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'date', 'calltime')
    search_fields = ('title', 'project__name')
    list_filter = ('date', 'project')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'call_sheet', 'time')
    search_fields = ('title', 'call_sheet__title')
    list_filter = ('call_sheet',)

@admin.register(Scenes)
class ScenesAdmin(admin.ModelAdmin):
    list_display = ('scene_number', 'call_sheet', 'location', 'page_count')
    search_fields = ('scene_number', 'call_sheet__title')
    list_filter = ('call_sheet', 'location')

@admin.register(Characters)
class CharactersAdmin(admin.ModelAdmin):
    list_display = ('character_name', 'actor', 'call_sheet', 'arrival', 'on_set')
    search_fields = ('character_name', 'actor', 'call_sheet__title')
    list_filter = ('call_sheet', 'character_name')

@admin.register(Extras)
class ExtrasAdmin(admin.ModelAdmin):
    list_display = ('extra', 'scene_number', 'call_sheet', 'arrival', 'on_set')
    search_fields = ('extra', 'scene_number', 'call_sheet__title')
    list_filter = ('call_sheet', 'scene_number')

@admin.register(DepartmentInstructions)
class DepartmentInstructionsAdmin(admin.ModelAdmin):
    list_display = ('department', 'call_sheet')
    search_fields = ('department', 'call_sheet__title')
    list_filter = ('call_sheet', 'department')