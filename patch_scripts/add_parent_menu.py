import re

with open('users/models.py', 'r') as f:
    content = f.read()

old_menu_model = """class MasterMenu(models.Model):
    menu_id = models.AutoField(primary_key=True, db_column='MenuId')
    menu_name = models.CharField(max_length=255, db_column='MenuName')
    url_page = models.CharField(max_length=255, db_column='UrlPage')
    view_access = models.BooleanField(default=False, db_column='ViewAccess')"""

new_menu_model = """class MasterMenu(models.Model):
    menu_id = models.AutoField(primary_key=True, db_column='MenuId')
    parent_menu = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='submenus', db_column='ParentMenuId')
    menu_name = models.CharField(max_length=255, db_column='MenuName')
    url_page = models.CharField(max_length=255, db_column='UrlPage')
    view_access = models.BooleanField(default=False, db_column='ViewAccess')"""

if "parent_menu =" not in content:
    content = content.replace(old_menu_model, new_menu_model)
    with open('users/models.py', 'w') as f:
        f.write(content)
