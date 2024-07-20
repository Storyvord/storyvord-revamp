# equipment/models.py
from django.db import models
from django.conf import settings

class EquipmentCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class EquipmentModel(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey('EquipmentCategory', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    specifications = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='equipment/images/', blank=True, null=True)

    def __str__(self):
        return self.name

class EquipmentInstance(models.Model):
    serial_number = models.CharField(max_length=50, unique=True)
    model = models.ForeignKey(EquipmentModel, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('available', 'Available'), ('maintenance', 'In Maintenance'), ('in_use', 'In Use')])
    location = models.CharField(max_length=100)
    last_maintenance_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.model.name} - {self.serial_number}"

class EquipmentLog(models.Model):
    equipment = models.ForeignKey(EquipmentInstance, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.equipment} - {self.action} by {self.user.username}"
