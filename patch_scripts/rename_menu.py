import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from users.models import MasterMenu

# Rename menu
menu = MasterMenu.objects.filter(menu_name='Student Course').first()
if menu:
    menu.menu_name = 'Allocation Details'
    menu.save()
    print("Renamed menu to Allocation Details")
