from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion

def set_created_by(apps, schema_editor):
    Folder = apps.get_model('files', 'Folder')
    User = apps.get_model(settings.AUTH_USER_MODEL)
    for folder in Folder.objects.all():
        if folder.project and folder.project.user:
            folder.created_by = folder.project.user
        else:
            folder.created_by = User.objects.first()  # Or another default user
        folder.save()

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('files', '0005_remove_file_allowed_users_folder_allowed_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_folders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RunPython(set_created_by),  # Populate the created_by field
        migrations.AlterField(
            model_name='folder',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_folders', to=settings.AUTH_USER_MODEL),
        ),
    ]
