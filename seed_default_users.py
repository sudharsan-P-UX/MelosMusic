import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from users.models import User, Role, RoleGroup

def create_users():
    # Ensure role groups exist
    superadmin_rg, _ = RoleGroup.objects.get_or_create(role_group_name="Superadmin")
    admin_rg, _ = RoleGroup.objects.get_or_create(role_group_name="Admin")
    
    # Ensure roles exist
    superadmin_role, _ = Role.objects.get_or_create(role_name="Superadmin", defaults={'role_group': superadmin_rg})
    admin_role, _ = Role.objects.get_or_create(role_name="admin", defaults={'role_group': admin_rg})
    
    # Create Superadmin (login uses first_name as username)
    try:
        user1 = User.objects.get(first_name="Superadmin")
        print("Superadmin user already exists, updating password.")
        user1.password = "Admin@123"
        user1.role = superadmin_role
        user1.save()
    except User.DoesNotExist:
        user1 = User.objects.create(
            first_name="Superadmin",
            password="Admin@123",
            last_name="",
            display_name="Superadmin",
            email="superadmin@melosmusic.com",
            role=superadmin_role,
            is_active=True
        )
        print("Created Superadmin user.")

    # Create admin
    try:
        user2 = User.objects.get(first_name="admin")
        print("admin user already exists, updating password.")
        user2.password = "Admin@123"
        user2.role = admin_role
        user2.save()
    except User.DoesNotExist:
        user2 = User.objects.create(
            first_name="admin",
            password="Admin@123",
            last_name="",
            display_name="Admin",
            email="admin@melosmusic.com",
            role=admin_role,
            is_active=True
        )
        print("Created admin user.")

if __name__ == '__main__':
    create_users()
