# Generated by Django 5.0.6 on 2024-08-28 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0007_clientprofile_employee_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientcompanyprofile',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='clientcompanyprofile',
            name='fax',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='clientcompanyprofile',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='clientcompanyprofile',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
