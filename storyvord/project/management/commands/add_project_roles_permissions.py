from django.core.management.base import BaseCommand
from ...models import Permission, Role

class Command(BaseCommand):
    help = 'Add project permissions, roles, and assign permissions to roles'

    def handle(self, *args, **kwargs):
        # Define permissions
        permissions = [
            ("generate_project_requirement", "To generate project requirement"),
            ("view", "Can view project"),
            ("edit", "Can edit project"),
            ("add_members", "Can add members to project"),
            ("create_task", "Can create task"),
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

        # Define roles
        roles = [
            ("admin", "Admin has all the permissions", True),
            ("member", "Can view project", True),
        ]

        # Add roles
        for role, description, is_global in roles:
            r, created = Role.objects.get_or_create(
                name=role,
                description=description,
                is_global=is_global
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Role added successfully: {role}'))
            else:
                self.stdout.write(self.style.WARNING(f'Role already exists: {role}'))

        # Define role-permission relationships
        role_permissions = [
            ("admin", "generate_project_requirement"),
            ("admin", "view"),
            ("admin", "edit"),
            ("admin", "add_members"),
            ("admin", "create_task"),
            ("member", "view"),
        ]

        # Function to add permission to role
        def add_permission_to_role(role_name, permission_name):
            try:
                role = Role.objects.get(name=role_name)
                permission = Permission.objects.get(name=permission_name)
                role.permission.add(permission)
                self.stdout.write(self.style.SUCCESS(f'Permission {permission_name} added to role {role_name}'))
            except Role.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Role {role_name} does not exist'))
            except Permission.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Permission {permission_name} does not exist'))

        # Add permissions to roles
        for role, permission in role_permissions:
            add_permission_to_role(role, permission)
