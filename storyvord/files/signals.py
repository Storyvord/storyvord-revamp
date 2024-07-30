from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from files.models import Folder  # Import Folder model
from project.models import Project  # Import Project model

@receiver(post_save, sender=Project)
def create_project_folders(sender, instance, created, **kwargs):
    if created:
        
        # Create Folder instances
        folder1 = Folder(name='Contracts', 
                         description= 'You can find contracts for actors, insurances, and more here.', 
                         icon= '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-book-open-text"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path><path d="M6 8h2"></path><path d="M6 12h2"></path><path d="M16 8h2"></path><path d="M16 12h2"></path></svg>',
                         project=instance,
                         default=True)
        folder2 = Folder(name='Scripts & Development', 
                         description= 'You can find everything related to development here.',
                         icon= '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-square-plus"><rect width="18" height="18" x="3" y="3" rx="2"></rect><path d="M8 12h8"></path><path d="M12 8v8"></path></svg>',
                         project=instance, 
                         default=True)
        folder3 = Folder(name='Sent Call Sheets', 
                         description= 'You can find copies of your call sheets here after sending them to your crew.',
                         icon= '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-file-spreadsheet"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"></path><path d="M14 2v4a2 2 0 0 0 2 2h4"></path><path d="M8 13h2"></path><path d="M14 13h2"></path><path d="M8 17h2"></path><path d="M14 17h2"></path></svg>',
                         project=instance, 
                         default=True)
        
        folder1.save()
        folder2.save()
        folder3.save()