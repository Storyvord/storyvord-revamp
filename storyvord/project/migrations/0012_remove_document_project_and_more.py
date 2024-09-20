# Generated by Django 5.0.6 on 2024-09-20 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0011_alter_document_document'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='project',
        ),
        migrations.RemoveField(
            model_name='project',
            name='uploaded_document',
        ),
        migrations.AddField(
            model_name='project',
            name='documents',
            field=models.ManyToManyField(related_name='documents', to='project.document'),
        ),
    ]
