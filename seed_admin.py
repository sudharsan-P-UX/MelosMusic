import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from users.models import RoleGroup, Role, User

def create_superadmin():
    # Create Role Group
    rg, _ = RoleGroup.objects.get_or_create(role_group_name="Administration")

    # Create Role
    role, _ = Role.objects.get_or_create(role_name="SuperAdmin", role_group=rg)

    # Create User
    user, created = User.objects.get_or_create(
        first_name="Sudharsan", # We'll use this as the Username
        defaults={
            "last_name": "SuperAdmin",
            "display_name": "Sudharsan",
            "email": "sudharsan@melosmusic.com",
            "phone": "0000000000",
            "password": "Admin123", # Plaintext for now based on your BRD
            "role": role,
            "is_active": True
        }
    )
    
    if created:
        print("SuperAdmin User 'Sudharsan' created successfully!")
    else:
        print("SuperAdmin User 'Sudharsan' already exists.")

if __name__ == '__main__':
    create_superadmin()
