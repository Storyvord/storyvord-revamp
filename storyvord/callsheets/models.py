# callsheets/models.py
from django.db import models
from project.models import Project
from crew.models import CrewProfile

class CallSheet(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    date = models.DateField(null=True, blank=True)
    calltime = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    nearest_hospital_address = models.CharField(max_length=255, blank=True)
    nearest_police_station = models.CharField(max_length=255, blank=True)
    nearest_fire_station = models.CharField(max_length=255, blank=True)
    additional_notes = models.TextField(blank=True, null=True)
    production_notes = models.TextField(blank=True, null=True)
    breakfast = models.TimeField(null=True, blank=True)
    lunch = models.TimeField(null=True, blank=True)
    dinner = models.TimeField(null=True, blank=True)
    allowed_users = models.ManyToManyField('accounts.User', related_name='callsheets', blank=True)

    def __str__(self):
        return self.title

class Event(models.Model):
    call_sheet = models.ForeignKey(CallSheet, on_delete=models.CASCADE, related_name='events')
    time = models.TimeField()
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class CallTime(models.Model):
    call_sheet = models.ForeignKey(CallSheet, on_delete=models.CASCADE, related_name='call_time')
    # name = models.CharField(max_length=255)
    position = models.CharField(max_length=255, null=True, blank=True)
    calltime = models.TimeField()
    # email = models.EmailField()
    # phone = models.CharField(max_length=255)
    remarks = models.TextField(blank=True, null=True)
    crew_profile = models.ForeignKey(CrewProfile, on_delete=models.CASCADE, related_name='call_times', blank=True, null=True)

    
    def __str__(self):
        return self.name

# class Scenes(models.Model):
#     call_sheet = models.ForeignKey(CallSheet, on_delete=models.CASCADE, related_name='scenes')
#     scene_number = models.CharField(max_length=255)
#     description = models.TextField(blank=True, null=True)
#     page_count = models.IntegerField(blank=True, null=True)
#     cast = models.TextField()
#     location = models.CharField(max_length=255)
#     other_notes = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return self.scene_number

# class Characters(models.Model):
#     call_sheet = models.ForeignKey(CallSheet, on_delete=models.CASCADE, related_name='characters')
#     character_name = models.CharField(max_length=255)
#     actor = models.CharField(max_length=255, blank=True)
#     status = models.TimeField(blank=True, null=True)
#     pickup = models.TimeField(blank=True, null=True)
#     arrival = models.TimeField(blank=True, null=True)
#     makeup = models.TimeField(blank=True, null=True)
#     costume = models.TimeField(blank=True, null=True)
#     rehearsal = models.TimeField(blank=True, null=True)
#     on_set = models.TimeField(blank=True, null=True)
#     info = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return self.character_name

# class Extras(models.Model):
#     call_sheet = models.ForeignKey(CallSheet, on_delete=models.CASCADE, related_name='extras')
#     scene_number = models.CharField(max_length=255)
#     extra = models.CharField(max_length=255)
#     arrival = models.TimeField(blank=True, null=True)
#     makeup = models.TimeField(blank=True, null=True)
#     costume = models.TimeField(blank=True, null=True)
#     rehearsal = models.TimeField(blank=True, null=True)
#     on_set = models.TimeField(blank=True, null=True)

#     def __str__(self):
#         return self.extra

# class DepartmentInstructions(models.Model):
#     call_sheet = models.ForeignKey(CallSheet, on_delete=models.CASCADE, related_name='department_instructions')
#     department = models.CharField(max_length=255)
#     instructions = models.TextField()

#     def __str__(self):
#         return self.department

class Weather(models.Model):
    call_sheet = models.ForeignKey(CallSheet, on_delete=models.CASCADE, related_name='weather')
    temperature = models.IntegerField()
    conditions = models.CharField(max_length=255)
    sunrise = models.TimeField(null=True, blank=True)
    sunset = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.temperature}°C - {self.conditions}"