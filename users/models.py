from django.db import models

class RoleGroup(models.Model):
    role_group_id = models.AutoField(primary_key=True, db_column='RoleGroupId')
    role_group_name = models.CharField(max_length=255, db_column='RoleGroupName')
    is_active = models.BooleanField(default=True, db_column='IsActive')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')
    created_by = models.IntegerField(null=True, blank=True, db_column='CreatedBy')

    class Meta:
        db_table = 'RoleGroup'

class Role(models.Model):
    role_id = models.AutoField(primary_key=True, db_column='RoleId')
    role_name = models.CharField(max_length=255, db_column='RoleName')
    role_group = models.ForeignKey(RoleGroup, on_delete=models.CASCADE, db_column='RoleGroupId')
    is_active = models.BooleanField(default=True, db_column='IsActive')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')
    created_by = models.IntegerField(null=True, blank=True, db_column='CreatedBy')

    class Meta:
        db_table = 'Role'

class MasterMenu(models.Model):
    menu_id = models.AutoField(primary_key=True, db_column='MenuId')
    parent_menu = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='submenus', db_column='ParentMenuId')
    menu_name = models.CharField(max_length=255, db_column='MenuName')
    url_page = models.CharField(max_length=255, db_column='UrlPage')
    view_access = models.BooleanField(default=False, db_column='ViewAccess')
    add_access = models.BooleanField(default=False, db_column='AddAccess')
    edit_access = models.BooleanField(default=False, db_column='EditAccess')
    delete_access = models.BooleanField(default=False, db_column='DeleteAccess')
    export_access = models.BooleanField(default=False, db_column='ExportAccess')
    approve_access = models.BooleanField(default=False, db_column='ApproveAccess')
    is_active = models.BooleanField(default=True, db_column='IsActive')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')
    created_by = models.IntegerField(null=True, blank=True, db_column='CreatedBy')

    class Meta:
        db_table = 'MasterMenu'

class MasterSubMenu(models.Model):
    sub_menu_id = models.AutoField(primary_key=True, db_column='SubMenuId')
    menu = models.ForeignKey(MasterMenu, on_delete=models.CASCADE, db_column='MenuId')
    menu_name = models.CharField(max_length=255, db_column='MenuName')
    url_page = models.CharField(max_length=255, db_column='UrlPage')
    view_access = models.BooleanField(default=False, db_column='ViewAccess')
    add_access = models.BooleanField(default=False, db_column='AddAccess')
    edit_access = models.BooleanField(default=False, db_column='EditAccess')
    delete_access = models.BooleanField(default=False, db_column='DeleteAccess')
    export_access = models.BooleanField(default=False, db_column='ExportAccess')
    approve_access = models.BooleanField(default=False, db_column='ApproveAccess')
    is_active = models.BooleanField(default=True, db_column='IsActive')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')
    created_by = models.IntegerField(null=True, blank=True, db_column='CreatedBy')

    class Meta:
        db_table = 'MasterSubMenu'

class RoleAccess(models.Model):
    role_access_id = models.AutoField(primary_key=True, db_column='RoleAccessId')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, db_column='RoleId')
    menu = models.ForeignKey(MasterMenu, on_delete=models.CASCADE, db_column='MenuId')
    view_access = models.BooleanField(default=False, db_column='ViewAccess')
    add_access = models.BooleanField(default=False, db_column='AddAccess')
    edit_access = models.BooleanField(default=False, db_column='EditAccess')
    delete_access = models.BooleanField(default=False, db_column='DeleteAccess')
    export_access = models.BooleanField(default=False, db_column='ExportAccess')
    approve_access = models.BooleanField(default=False, db_column='ApproveAccess')
    is_active = models.BooleanField(default=True, db_column='IsActive')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')
    created_by = models.IntegerField(null=True, blank=True, db_column='CreatedBy')

    class Meta:
        db_table = 'RoleAccess'


class User(models.Model):
    user_id = models.AutoField(primary_key=True, db_column='UserId')
    first_name = models.CharField(max_length=255, db_column='Firstname')
    last_name = models.CharField(max_length=255, db_column='Lastname')
    display_name = models.CharField(max_length=255, db_column='Displayname')
    email = models.EmailField(db_column='Email')
    phone = models.CharField(max_length=50, db_column='Phone')
    user_code = models.CharField(max_length=50, null=True, blank=True, db_column='UserCode')
    gender = models.CharField(max_length=20, null=True, blank=True, db_column='Gender')
    dob = models.DateField(null=True, blank=True, db_column='DOB')
    address = models.CharField(max_length=500, null=True, blank=True, db_column='Address')
    parent_name = models.CharField(max_length=200, null=True, blank=True, db_column='ParentName')
    parent_phone = models.CharField(max_length=20, null=True, blank=True, db_column='ParentPhone')
    preferred_days = models.CharField(max_length=200, null=True, blank=True, db_column='PreferredDays')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, db_column='RoleId')
    is_active = models.BooleanField(default=True, db_column='IsActive')
    password = models.CharField(max_length=255, db_column='Password')
    salt_key = models.CharField(max_length=255, db_column='SaltKey', null=True, blank=True)
    is_changed = models.BooleanField(default=False, db_column='IsChanged')
    password_change_date = models.DateTimeField(null=True, blank=True, db_column='PasswordChangeDate')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')
    created_by = models.IntegerField(null=True, blank=True, db_column='CreatedBy')
    last_date = models.DateTimeField(auto_now=True, db_column='LastDate')
    last_changed_by = models.IntegerField(null=True, blank=True, db_column='LastChangedBy')

    class Meta:
        db_table = 'Users'

class UserAddress(models.Model):
    user_address_id = models.AutoField(primary_key=True, db_column='UserAddressId')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='UserId')
    address_line_1 = models.CharField(max_length=1000, db_column='AddressLine1')
    address_line_2 = models.CharField(max_length=1000, null=True, blank=True, db_column='AddressLine2')
    city = models.CharField(max_length=255, db_column='City')
    state = models.CharField(max_length=255, db_column='State')
    country = models.IntegerField(db_column='Country')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')
    created_by = models.IntegerField(null=True, blank=True, db_column='CreatedBy')
    last_date = models.DateTimeField(auto_now=True, db_column='LastDate')
    last_changed_by = models.IntegerField(null=True, blank=True, db_column='LastChangedBy')

    class Meta:
        db_table = 'UserAddress'

class UserLoginDetails(models.Model):
    user_login_details_id = models.AutoField(primary_key=True, db_column='UserLoginDetails')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='UserId')
    login_date = models.DateTimeField(auto_now_add=True, db_column='LoginDate')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')
    created_by = models.IntegerField(null=True, blank=True, db_column='CreatedBy')
    remarks = models.TextField(null=True, blank=True, db_column='Remarks')

    class Meta:
        db_table = 'UserLoginDetails'


class UserQualification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='qualifications')
    institution = models.CharField(max_length=255)
    qualification = models.CharField(max_length=255)
    passed_year = models.IntegerField()
    gpa = models.CharField(max_length=50)

    class Meta:
        db_table = 'UserQualification'


class UserCertification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certifications')
    certificate_name = models.CharField(max_length=255)
    year = models.IntegerField()
    document = models.FileField(upload_to='certifications/', null=True, blank=True)

    class Meta:
        db_table = 'UserCertification'

class UserExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiences')
    company_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    from_date = models.DateField()
    to_date = models.DateField()
    years_of_experience = models.DecimalField(max_digits=5, decimal_places=1)

    class Meta:
        db_table = 'UserExperience'
