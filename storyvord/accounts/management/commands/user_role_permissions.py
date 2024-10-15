from django.core.management.base import BaseCommand
from ...models import Permission, UserType

class Command(BaseCommand):
    help = 'Add User permissions, User types, and assign permissions to user types'

    def handle(self, *args, **kwargs):
        # Define permissions
        permissions = [
            ("create_project", "User with this permission has permission to create project."),
        ]

        # Add permissions
        for permission, description in permissions:
            perm, created = Permission.objects.get_or_create(
                name=permission,
                description=description
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Permission added successfully: {permission}'))
            else:
                self.stdout.write(self.style.WARNING(f'Permission already exists: {permission}'))

        # Define user types
        user_types = [
            ("client", "client user"),
            ("crew", "crew user"),
        ]

        # Add roles
        for usertype, description in user_types:
            r, created = UserType.objects.get_or_create(
                name=usertype,
                description=description,
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'UserType added successfully: {usertype}'))
            else:
                self.stdout.write(self.style.WARNING(f'UserType already exists: {usertype}'))

        # Define role-permission relationships
        usertype_permissions = [
            ("client", "create_project")
        ]

        # Function to add permission to role
        def add_permission_to_role(usertype_name, permission_name):
            try:
                usertype = UserType.objects.get(name=usertype_name)
                permission = Permission.objects.get(name=permission_name)
                usertype.permissions.add(permission)
                self.stdout.write(self.style.SUCCESS(f'Permission {permission_name} added to role {usertype}'))
            except UserType.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Role {usertype_name} does not exist'))
            except Permission.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Permission {permission_name} does not exist'))

        # Add permissions to roles
        for usertype, permission in usertype_permissions:
            add_permission_to_role(usertype, permission)
