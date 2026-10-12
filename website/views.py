from django.shortcuts import render, redirect
from django.contrib import messages
from users.models import User, UserLoginDetails

from academics.models import Course
from finance.models import StudentFeeInstallment
from django.db.models import Sum, F

def index(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    # Fetch user for dashboard display
    try:
        try:

            user = User.objects.get(user_id=request.session['user_id'])

        except User.DoesNotExist:

            request.session.flush()

            return redirect('login')
    except User.DoesNotExist:
        request.session.flush()
        return redirect('login')
    
    # Dashboard metrics
    total_students = User.objects.filter(role__role_name__iexact='student').count()
    active_teachers = User.objects.filter(role__role_name__iexact='teacher').count()
    total_courses = Course.objects.filter(is_active=True).count()
    
    pending_fees = StudentFeeInstallment.objects.filter(amount__gt=F('paid_amount')).aggregate(
        total_pending=Sum(F('amount') - F('paid_amount'))
    )['total_pending'] or 0
    
    context = {
        'user': user,
        'total_students': total_students,
        'active_teachers': active_teachers,
        'total_courses': total_courses,
        'pending_fees': pending_fees,
    }
    return render(request, 'website/index.html', context)

def login_view(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        upass = request.POST.get('password')
        
        try:
            # We treat first_name as the username based on your setup
            user = User.objects.get(first_name=uname, password=upass)
            if user.is_active:
                request.session['user_id'] = user.user_id
                # Log the successful login
                UserLoginDetails.objects.create(user=user, remarks="Success")
                return redirect('index')
            else:
                error = "Account is disabled."
                UserLoginDetails.objects.create(user=user, remarks="Failed: Disabled")
                return render(request, 'website/login.html', {'error': error})
        except User.DoesNotExist:
            error = "Invalid username or password."
            return render(request, 'website/login.html', {'error': error})
            
    return render(request, 'website/login.html')

def logout_view(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('login')

def students_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    try:

    
        user = User.objects.get(user_id=request.session['user_id'])

    
    except User.DoesNotExist:

    
        request.session.flush()

    
        return redirect('login')
    from academics.models import Course, Batch, StudentEnrollment
    from users.models import Role, RoleGroup
    
    courses = Course.objects.filter(is_active=True)
    batches = Batch.objects.filter(is_active=True)
    
    rg, _ = RoleGroup.objects.get_or_create(role_group_name="Students")
    student_role, _ = Role.objects.get_or_create(role_name="Student", defaults={'role_group': rg})
    
    if request.method == 'POST':
        name = request.POST.get('student_name')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        parent_name = request.POST.get('parent_name')
        parent_phone = request.POST.get('parent_phone')
        
        course_id = request.POST.get('course_id')
        batch_id = request.POST.get('batch_id')
        joining_date = request.POST.get('joining_date')
        
        status = request.POST.get('status') == '1'
        password = request.POST.get('password')
        
        confirm_password = request.POST.get('confirm_password')
        if password and password != confirm_password:
            messages.error(request, "Password and confirm password must match.")
            return redirect('students')
        
        days_list = request.POST.getlist('days')
        preferred_days = ', '.join(days_list) if days_list else request.POST.get('days', '')
        
        parts = name.split(' ', 1)
        fname = parts[0]
        lname = parts[1] if len(parts) > 1 else ""
        
        user_code = "S1000"
        last_student = User.objects.filter(role=student_role, user_code__startswith='S').order_by('-user_id').first()
        if last_student and last_student.user_code:
            try:
                user_code = f"S{int(last_student.user_code[1:]) + 1}"
            except: pass
            
        # Uniqueness checks

            
        if User.objects.filter(first_name__iexact=fname).exists():

            
            messages.error(request, "Username (First Name) already exists.")

            
            return redirect('students')

            
        if User.objects.filter(email__iexact=email).exists():

            
            messages.error(request, "Email already exists.")

            
            return redirect('students')

            
        if User.objects.filter(phone=phone).exists():

            
            messages.error(request, "Phone already exists.")

            
            return redirect('students')

            
        new_student = User.objects.create(
            user_code=user_code,
            first_name=fname,
            last_name=lname,
            display_name=name,
            email=email,
            phone=phone,
            gender=gender,
            dob=dob if dob else None,
            address=address,
            parent_name=parent_name,
            parent_phone=parent_phone,
            is_active=status,
            role=student_role,
            password=password,
            preferred_days=preferred_days
        )
        

            
        messages.success(request, 'Student added successfully!')
        return redirect('students')
        
    students = User.objects.filter(role=student_role)
    
    # Filter logic
    search = request.GET.get('search', '')
    gender = request.GET.get('gender', '')
    status_filter = request.GET.get('status_filter', '')
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')
    
    from django.db.models import Q
    
    if search:
        students = students.filter(
            Q(first_name__icontains=search) | 
            Q(last_name__icontains=search) |
            Q(display_name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search)
        )
        
    if gender:
        students = students.filter(gender=gender)
        
    if status_filter != '':
        students = students.filter(is_active=(status_filter == '1'))
        
    if from_date:
        students = students.filter(created_date__date__gte=from_date)
        
    if to_date:
        students = students.filter(created_date__date__lte=to_date)
        
    students = students.order_by('-user_id')
        
    return render(request, 'website/students.html', {
        'user': user,
        'courses': courses,
        'batches': batches,
        'students': students,
        'page_title': 'Student Profile'
    })

def update_student(request, student_id):
    if 'user_id' not in request.session:
        return redirect('login')
        
    if request.method == 'POST':
        try:
            student = User.objects.get(user_id=student_id)
            name = request.POST.get('student_name')
            parts = name.split(' ', 1)
            fname = parts[0]

            email = request.POST.get('email')

            phone = request.POST.get('phone')

            if User.objects.filter(first_name__iexact=fname).exclude(user_id=student_id).exists():

                messages.error(request, "Username (First Name) already exists.")

                return redirect('students')

            if User.objects.filter(email__iexact=email).exclude(user_id=student_id).exists():

                messages.error(request, "Email already exists.")

                return redirect('students')

            if User.objects.filter(phone=phone).exclude(user_id=student_id).exists():

                messages.error(request, "Phone already exists.")

                return redirect('students')

            student.first_name = parts[0]
            student.last_name = parts[1] if len(parts) > 1 else ""
            student.display_name = name
            
            student.email = request.POST.get('email')
            student.phone = request.POST.get('phone')
            student.is_active = request.POST.get('status') == '1'
            
            days_list = request.POST.getlist('days')
            student.preferred_days = ', '.join(days_list) if days_list else ''
            
            password = request.POST.get('password')
            if password:
                confirm_password = request.POST.get('confirm_password')
                if password != confirm_password:
                    messages.error(request, "Password and confirm password must match.")
                    return redirect('students')
                student.password = password
                    
            student.save()
            

        except User.DoesNotExist:
            pass
            
    return redirect('students')

def delete_student(request, student_id):
    if 'user_id' not in request.session:
        return redirect('login')
    try:
        User.objects.get(user_id=student_id).delete()
    except User.DoesNotExist:
        pass
    return redirect('students')

def teachers_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    try:

    
        user = User.objects.get(user_id=request.session['user_id'])

    
    except User.DoesNotExist:

    
        request.session.flush()

    
        return redirect('login')
    from academics.models import Course, Batch, UserCourse
    from users.models import Role, RoleGroup
    
    courses = Course.objects.filter(is_active=True)
    batches = Batch.objects.filter(is_active=True)
    
    # Ensure a default role group and student role exist
    rg, _ = RoleGroup.objects.get_or_create(role_group_name="Teachers")
    teacher_role, _ = Role.objects.get_or_create(role_name="Teacher", defaults={'role_group': rg})
    
    if request.method == 'POST':
        name = request.POST.get('teacher_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        course_id = request.POST.get('course_id')
        status = request.POST.get('status') == '1'
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        days_list = request.POST.getlist('days')
        preferred_days = ', '.join(days_list) if days_list else ''
        
        # Simple validation
        if password and password != confirm_password:
            messages.error(request, "Password and confirm password must match.")
            return redirect('teachers')
        
        parts = name.split(' ', 1)
        fname = parts[0]
        lname = parts[1] if len(parts) > 1 else ""
        
        user_code = "T2000"
        last_teacher = User.objects.filter(role=teacher_role, user_code__startswith='T').order_by('-user_id').first()
        if last_teacher and last_teacher.user_code:
            try:
                user_code = f"T{int(last_teacher.user_code[1:]) + 1}"
            except: pass
            
        # Uniqueness checks

            
        if User.objects.filter(first_name__iexact=fname).exists():

            
            messages.error(request, "Username (First Name) already exists.")

            
            return redirect('teachers')

            
        if User.objects.filter(email__iexact=email).exists():

            
            messages.error(request, "Email already exists.")

            
            return redirect('teachers')

            
        if User.objects.filter(phone=phone).exists():

            
            messages.error(request, "Phone already exists.")

            
            return redirect('teachers')

            
        new_teacher = User.objects.create(
            user_code=user_code,
            first_name=fname,
            last_name=lname,
            display_name=name,
            email=email,
            phone=phone,
            is_active=status,
            role=teacher_role,
            password=password,
            preferred_days=preferred_days
        )
        
        # Save Educational Qualifications
        institutions = request.POST.getlist('edu_institution[]')
        qualifications = request.POST.getlist('edu_qualification[]')
        years = request.POST.getlist('edu_year[]')
        gpas = request.POST.getlist('edu_gpa[]')
        
        from users.models import UserQualification, UserExperience, UserCertification
        
        for i in range(len(institutions)):
            if institutions[i].strip():
                UserQualification.objects.create(
                    user=new_teacher,
                    institution=institutions[i],
                    qualification=qualifications[i] if i < len(qualifications) else '',
                    passed_year=int(years[i]) if i < len(years) and years[i] else 0,
                    gpa=gpas[i] if i < len(gpas) else ''
                )
                
        # Save Experiences
        companies = request.POST.getlist('exp_company[]')
        roles = request.POST.getlist('exp_role[]')
        from_dates = request.POST.getlist('exp_from[]')
        to_dates = request.POST.getlist('exp_to[]')
        exp_years = request.POST.getlist('exp_years[]')
        
        for i in range(len(companies)):
            if companies[i].strip() and i < len(from_dates) and from_dates[i]:
                UserExperience.objects.create(
                    user=new_teacher,
                    company_name=companies[i],
                    role=roles[i] if i < len(roles) else '',
                    from_date=from_dates[i],
                    to_date=to_dates[i] if i < len(to_dates) and to_dates[i] else from_dates[i],
                    years_of_experience=float(exp_years[i]) if i < len(exp_years) and exp_years[i] else 0.0
                )

        # Save Certifications
        cert_names = request.POST.getlist('cert_name[]')
        cert_years = request.POST.getlist('cert_year[]')
        cert_docs = request.FILES.getlist('cert_document[]')
        
        from users.models import UserCertification
        
        for i in range(len(cert_names)):
            if cert_names[i].strip():
                UserCertification.objects.create(
                    user=new_teacher,
                    certificate_name=cert_names[i],
                    year=int(cert_years[i]) if i < len(cert_years) and cert_years[i] else 0,
                    document=cert_docs[i] if i < len(cert_docs) else None
                )

        
        if course_id:
            course = Course.objects.get(course_id=course_id)
            UserCourse.objects.create(user=new_teacher, course=course)
            
        messages.success(request, 'Teacher added successfully!')
        return redirect('teachers')
        
    teachers = User.objects.filter(role=teacher_role).order_by('-user_id')
    
    # Filter logic for teachers
    search = request.GET.get('search', '')
    status_filter = request.GET.get('status_filter', '')
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')
    
    from django.db.models import Q
    
    if search:
        teachers = teachers.filter(
            Q(display_name__icontains=search) | 
            Q(email__icontains=search) | 
            Q(phone__icontains=search) |
            Q(user_code__icontains=search)
        )
        
    if status_filter != '':
        teachers = teachers.filter(is_active=(status_filter == '1'))
        
    if from_date:
        teachers = teachers.filter(created_date__gte=from_date)
        
    if to_date:
        teachers = teachers.filter(created_date__lte=to_date)
        
    return render(request, 'website/teachers.html', {
        'user': user,
        'courses': courses,
        'batches': batches,
        'teachers': teachers,
        'page_title': 'Teacher Management'
    })

def update_teacher(request, teacher_id):
    if 'user_id' not in request.session:
        return redirect('login')
        
    if request.method == 'POST':
        try:
            teacher = User.objects.get(user_id=teacher_id)
            name = request.POST.get('teacher_name')
            parts = name.split(' ', 1)
            fname = parts[0]

            email = request.POST.get('email')

            phone = request.POST.get('phone')

            if User.objects.filter(first_name__iexact=fname).exclude(user_id=teacher_id).exists():

                messages.error(request, "Username (First Name) already exists.")

                return redirect('teachers')

            if User.objects.filter(email__iexact=email).exclude(user_id=teacher_id).exists():

                messages.error(request, "Email already exists.")

                return redirect('teachers')

            if User.objects.filter(phone=phone).exclude(user_id=teacher_id).exists():

                messages.error(request, "Phone already exists.")

                return redirect('teachers')

            teacher.first_name = parts[0]
            teacher.last_name = parts[1] if len(parts) > 1 else ""
            teacher.display_name = name
            
            teacher.email = request.POST.get('email')
            teacher.phone = request.POST.get('phone')
            teacher.is_active = request.POST.get('status') == '1'
            
            days_list = request.POST.getlist('days')
            teacher.preferred_days = ', '.join(days_list) if days_list else ''
            
            password = request.POST.get('password')
            if password:
                confirm_password = request.POST.get('confirm_password')
                if password != confirm_password:
                    messages.error(request, "Password and confirm password must match.")
                    return redirect('teachers')
                teacher.password = password
                    
            teacher.save()

            from users.models import UserQualification, UserExperience, UserCertification
            UserQualification.objects.filter(user=teacher).delete()
            UserExperience.objects.filter(user=teacher).delete()
            
            institutions = request.POST.getlist('edu_institution[]')
            qualifications = request.POST.getlist('edu_qualification[]')
            years = request.POST.getlist('edu_year[]')
            gpas = request.POST.getlist('edu_gpa[]')
            for i in range(len(institutions)):
                if institutions[i].strip():
                    UserQualification.objects.create(
                        user=teacher,
                        institution=institutions[i],
                        qualification=qualifications[i] if i < len(qualifications) else '',
                        passed_year=int(years[i]) if i < len(years) and years[i] else 0,
                        gpa=gpas[i] if i < len(gpas) else ''
                    )
                    
            companies = request.POST.getlist('exp_company[]')
            roles = request.POST.getlist('exp_role[]')
            from_dates = request.POST.getlist('exp_from[]')
            to_dates = request.POST.getlist('exp_to[]')
            exp_years = request.POST.getlist('exp_years[]')
            for i in range(len(companies)):
                if companies[i].strip() and i < len(from_dates) and from_dates[i]:
                    UserExperience.objects.create(
                        user=teacher,
                        company_name=companies[i],
                        role=roles[i] if i < len(roles) else '',
                        from_date=from_dates[i],
                        to_date=to_dates[i] if i < len(to_dates) and to_dates[i] else from_dates[i],
                        years_of_experience=float(exp_years[i]) if i < len(exp_years) and exp_years[i] else 0.0
                    )

            UserCertification.objects.filter(user=teacher).delete()
            
            cert_names = request.POST.getlist('cert_name[]')
            cert_years = request.POST.getlist('cert_year[]')
            cert_docs = request.FILES.getlist('cert_document[]')
            
            for i in range(len(cert_names)):
                if cert_names[i].strip():
                    UserCertification.objects.create(
                        user=teacher,
                        certificate_name=cert_names[i],
                        year=int(cert_years[i]) if i < len(cert_years) and cert_years[i] else 0,
                        document=cert_docs[i] if i < len(cert_docs) else None
                    )
            
            # Update course if provided
            course_id = request.POST.get('course_id')
            if course_id:
                from academics.models import Course, UserCourse
                course = Course.objects.get(course_id=course_id)
                # Just update the first mapping for simplicity
                uc = UserCourse.objects.filter(user=teacher).first()
                if uc:
                    uc.course = course
                    uc.save()
                else:
                    UserCourse.objects.create(user=teacher, course=course)
        except User.DoesNotExist:
            pass
            
    messages.success(request, 'Teacher updated successfully!')
    return redirect('teachers')

def delete_teacher(request, teacher_id):
    if 'user_id' not in request.session:
        return redirect('login')
    try:
        User.objects.get(user_id=teacher_id).delete()
    except User.DoesNotExist:
        pass
    messages.success(request, 'Teacher deleted successfully!')
    return redirect('teachers')


def enrollment_management_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
        
    try:

        
        user = User.objects.get(user_id=request.session['user_id'])

        
    except User.DoesNotExist:

        
        request.session.flush()

        
        return redirect('login')
    from academics.models import Course, Batch, StudentEnrollment
    from users.models import Role, RoleGroup
    
    rg, _ = RoleGroup.objects.get_or_create(role_group_name="Students")
    student_role, _ = Role.objects.get_or_create(role_name="Student", defaults={'role_group': rg})
    
    students = User.objects.filter(role=student_role, is_active=True)
    courses = Course.objects.all()
    batches = Batch.objects.all()
    enrollments = StudentEnrollment.objects.all()
    
    from django.db.models import Count, Q
    
    course_stats = list(Course.objects.annotate(
        enroll_count=Count('studentenrollment', filter=Q(studentenrollment__status=1))
    ).values('course_name', 'enroll_count'))
    
    active_students = User.objects.filter(role=student_role, is_active=True).count()
    inactive_students = User.objects.filter(role=student_role, is_active=False).count()
    
    batch_stats = list(Batch.objects.annotate(
        enroll_count=Count('studentenrollment', filter=Q(studentenrollment__status=1))
    ).values('batch_name', 'capacity', 'enroll_count')[:5])
    
    return render(request, 'website/enrollment_management.html', {
        'course_stats': course_stats,
        'active_students': active_students,
        'inactive_students': inactive_students,
        'batch_stats': batch_stats,
        'user': user,
        'page_title': 'Enrollment Management',
        'students': students,
        'courses': courses,
        'batches': batches,
        'enrollments': enrollments
    })

def events_dashboard_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
        
    try:

        
        user = User.objects.get(user_id=request.session['user_id'])

        
    except User.DoesNotExist:

        
        request.session.flush()

        
        return redirect('login')
    
    from events.models import EventMaster, EventParticipant, EventVenue, EventAttendance
    from django.contrib import messages
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        # RBAC Check for POST actions
        if action == 'save_settings':
            import json, os
            from django.conf import settings
            
            phone_length = request.POST.get('phone_length', 10)
            email_length = request.POST.get('email_length', 255)
            password_expire = request.POST.get('password_expire', 90)
            attendance_from_date = request.POST.get('attendance_from_date', '').strip()
            attendance_to_date = request.POST.get('attendance_to_date', '').strip()
            
            data = {
                'phone_length': int(phone_length) if phone_length else 10,
                'email_length': int(email_length) if email_length else 255,
                'password_expire': int(password_expire) if password_expire else 90,
                'attendance_from_date': attendance_from_date,
                'attendance_to_date': attendance_to_date,
            }
            path = os.path.join(settings.BASE_DIR, 'security_settings.json')
            with open(path, 'w') as fh:
                json.dump(data, fh, indent=4)
            
            messages.success(request, 'Settings saved successfully.')
            return redirect('/admin-dashboard/?tab=settings')
            
        if action == 'create_user' and not admin_access.add_access:
            messages.error(request, 'You do not have permission to add records.')
            return redirect('/admin-dashboard/')
            
        if action == 'save_permissions' and not admin_access.edit_access:
            messages.error(request, 'You do not have permission to edit records.')
            return redirect('/admin-dashboard/')
            
        if action == 'save_menu_orders':
            if not admin_access.edit_access:
                messages.error(request, 'You do not have permission to edit records.')
                return redirect('/admin-dashboard/?tab=menu')
            
            for key, value in request.POST.items():
                if key.startswith('order_'):
                    menu_id = key.replace('order_', '')
                    try:
                        menu = MasterMenu.objects.get(menu_id=menu_id)
                        menu.display_order = int(value)
                        menu.save()
                    except Exception as e:
                        pass
            
            messages.success(request, 'Menu order updated successfully!')
            return redirect('/admin-dashboard/?tab=menu')

        if action == 'save_menu':
            if request.POST.get('menu_id') and not admin_access.edit_access:
                messages.error(request, 'You do not have permission to edit records.')
                return redirect('/admin-dashboard/?tab=menu')
            elif not request.POST.get('menu_id') and not admin_access.add_access:
                messages.error(request, 'You do not have permission to add records.')
                return redirect('/admin-dashboard/?tab=menu')
                
        if action == 'delete_menu' and not admin_access.delete_access:
            messages.error(request, 'You do not have permission to delete records.')
            return redirect('/admin-dashboard/?tab=menu')

        if action == 'add_venue':
            venue_name = request.POST.get('venue_name')
            capacity = request.POST.get('capacity')
            address = request.POST.get('address')
            
            capacity_val = capacity if capacity else None
            
            EventVenue.objects.create(
                venue_name=venue_name,
                capacity=capacity_val,
                address=address
            )
            messages.success(request, 'Venue added successfully!')
            return redirect('/events/?tab=venue')
    
    events = EventMaster.objects.all().order_by('-event_date')
    
    search = request.GET.get('search')
    if search:
        events = events.filter(event_name__icontains=search)
        
    event_type = request.GET.get('type')
    if event_type:
        events = events.filter(event_type=event_type)
        
    status = request.GET.get('status')
    if status:
        events = events.filter(status=status)
        
    from_date = request.GET.get('from_date')
    if from_date:
        events = events.filter(event_date__gte=from_date)
        
    to_date = request.GET.get('to_date')
    if to_date:
        events = events.filter(event_date__lte=to_date)
    venues = EventVenue.objects.all()
    participants = EventParticipant.objects.all()
    attendance = EventAttendance.objects.all()
    
    tab = request.GET.get('tab', 'calendar')
    
    event_id = request.GET.get('event_id')
    selected_event = None
    if event_id:
        try:
            selected_event = EventMaster.objects.get(event_id=event_id)
        except:
            pass
    elif events.exists():
        selected_event = events.first()
        
    edit_mode = request.GET.get('edit', 'false') == 'true'
    
    return render(request, 'website/events_dashboard.html', {
        'edit_mode': edit_mode,
        'user': user,
        'page_title': 'Event Scheduling',
        'events': events,
        'venues': venues,
        'participants': participants,
        'attendance': attendance,
        'active_tab': tab,
        'selected_event': selected_event
    })

def create_event_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
        
    if request.method == 'POST':
        from events.models import EventMaster, EventVenue
        from users.models import User
        
        try:

        
            user = User.objects.get(user_id=request.session['user_id'])

        
        except User.DoesNotExist:

        
            request.session.flush()

        
            return redirect('login')
        
        event_id = request.POST.get('event_id') # For editing
        
        event_name = request.POST.get('event_name')
        event_type = request.POST.get('event_type')
        event_date = request.POST.get('event_date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        venue_id = request.POST.get('venue_id')
        status = request.POST.get('status')
        description = request.POST.get('description')
        
        organizer = request.POST.get('organizer')
        contact_person = request.POST.get('contact_person')
        contact_phone = request.POST.get('contact_phone')
        reg_start = request.POST.get('registration_start_date')
        reg_end = request.POST.get('registration_end_date')
        max_participants = request.POST.get('max_participants')
        
        venue = None
        if venue_id and venue_id != '0':
            try:
                venue = EventVenue.objects.get(venue_id=venue_id)
            except:
                pass
                
        if event_id:
            # Update existing
            event = EventMaster.objects.get(event_id=event_id)
            event.event_name = event_name
            event.event_type = event_type
            event.event_date = event_date
            event.start_time = start_time
            event.end_time = end_time
            event.venue = venue
            event.status = status
            event.description = description
            event.organizer = organizer
            event.contact_person = contact_person
            event.contact_phone = contact_phone
            event.registration_start_date = reg_start if reg_start else None
            event.registration_end_date = reg_end if reg_end else None
            event.max_participants = max_participants if max_participants else None
            event.save()
            
            from django.contrib import messages
            messages.success(request, 'Event updated successfully!')
        else:
            # Create new
            event = EventMaster.objects.create(
                event_name=event_name,
                event_type=event_type,
                event_date=event_date,
                start_time=start_time,
                end_time=end_time,
                venue=venue,
                status=status,
                description=description,
                organizer=organizer,
                contact_person=contact_person,
                contact_phone=contact_phone,
                registration_start_date=reg_start if reg_start else None,
                registration_end_date=reg_end if reg_end else None,
                max_participants=max_participants if max_participants else None,
                created_by=user
            )
            
            from django.contrib import messages
            messages.success(request, 'Event added successfully!')
            
        return redirect('/events/?tab=list')
        
    return redirect('/events/?tab=create')

def generic_page(request, page_name):
    redirect_map = {
        'courses': 'courses',
        'fees': 'pending_fees',
        'students': 'students',
        'teachers': 'teachers',
        'timetable': 'timetable',
        'events': 'events_dashboard',
        'attendance': 'student_attendance',
    }
    if page_name in redirect_map:
        return redirect(redirect_map[page_name])

    if 'user_id' not in request.session:
        return redirect('login')
        
    try:

        
        user = User.objects.get(user_id=request.session['user_id'])

        
    except User.DoesNotExist:

        
        request.session.flush()

        
        return redirect('login')
    
    # Map the URL path to a display title
    titles = {
        'students': 'Student Profile',
        'attendance': 'Attendance',
        'fees': 'Fees',
        'events': 'Event Scheduling',
        'courses': 'Courses & Batches',
        'teachers': 'Teacher Management',
        'timetable': 'Timetable',
        'notifications': 'Notifications / Reminders',
        'reports': 'Reports'
    }
    
    title = titles.get(page_name, page_name.replace('-', ' ').title())
    return render(request, 'website/generic_page.html', {'user': user, 'page_title': title})


def sync_batch_timetable(created_by_id=None):
    try:
        from academics.models import Batch, Timetable, Course

        all_class_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

        day_map = {
            'mon': 'Monday', 'monday': 'Monday',
            'tue': 'Tuesday', 'tues': 'Tuesday', 'tuesday': 'Tuesday',
            'wed': 'Wednesday', 'wednesday': 'Wednesday',
            'thu': 'Thursday', 'thur': 'Thursday', 'thurs': 'Thursday', 'thursday': 'Thursday',
            'fri': 'Friday', 'friday': 'Friday',
            'sat': 'Saturday', 'saturday': 'Saturday',
            'sun': 'Sunday', 'sunday': 'Sunday'
        }

        for batch in Batch.objects.select_related('course', 'teacher').filter(is_active=True):
            if not (batch.start_time and batch.end_time and batch.teacher):
                continue

            course_days = []
            if batch.course and batch.course.days:
                raw_text = batch.course.days.lower()
                if 'all' in raw_text or 'every' in raw_text:
                    course_days = list(all_class_days)
                else:
                    raw_days = [d.strip() for d in batch.course.days.replace(';', ',').split(',') if d.strip()]
                    for rd in raw_days:
                        clean = day_map.get(rd.lower())
                        if clean and clean not in course_days:
                            course_days.append(clean)

            if not course_days:
                course_days = list(all_class_days)

            room = f"Studio {batch.batch_code}" if batch.batch_code else "Studio 1"

            # Remove obsolete slots for days not in this course's schedule
            Timetable.objects.filter(batch=batch).exclude(day_of_week__in=course_days).delete()

            for day in course_days:
                slot, created = Timetable.objects.get_or_create(
                    batch=batch,
                    day_of_week=day,
                    defaults={
                        'teacher': batch.teacher,
                        'start_time': batch.start_time,
                        'end_time': batch.end_time,
                        'room_number': room,
                        'is_active': True,
                        'created_by': created_by_id
                    }
                )
                if not created:
                    updated = False
                    if slot.teacher != batch.teacher:
                        slot.teacher = batch.teacher
                        updated = True
                    if slot.start_time != batch.start_time or slot.end_time != batch.end_time:
                        slot.start_time = batch.start_time
                        slot.end_time = batch.end_time
                        updated = True
                    if slot.room_number != room:
                        slot.room_number = room
                        updated = True
                    if not slot.is_active:
                        slot.is_active = True
                        updated = True
                    if updated:
                        slot.save()
    except Exception as e:
        print(f"Error syncing batch timetable: {e}")


def timetable_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    try:
        user = User.objects.get(user_id=request.session['user_id'])
    except User.DoesNotExist:
        request.session.flush()
        return redirect('login')
        
    from academics.models import Timetable, Batch, Course, StudentEnrollment
    from django.db.models import Q
    
    sync_batch_timetable(user.user_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'edit_slot':
            slot_id = request.POST.get('slot_id')
            batch_id = request.POST.get('batch_id')
            teacher_id = request.POST.get('teacher_id')
            day_of_week = request.POST.get('day_of_week')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            room_number = request.POST.get('room_number')
            try:
                slot = Timetable.objects.get(timetable_id=slot_id)
                if batch_id:
                    slot.batch = Batch.objects.get(batch_id=batch_id)
                if teacher_id:
                    slot.teacher = User.objects.get(user_id=teacher_id)
                if day_of_week:
                    slot.day_of_week = day_of_week
                if start_time:
                    slot.start_time = start_time
                if end_time:
                    slot.end_time = end_time
                slot.room_number = room_number
                slot.save()
                messages.success(request, 'Timetable slot updated successfully!')
            except Exception as e:
                messages.error(request, f'Error updating slot: {str(e)}')
            return redirect('timetable')
            
        elif action == 'delete_slot':
            slot_id = request.POST.get('slot_id')
            try:
                Timetable.objects.filter(timetable_id=slot_id).delete()
                messages.success(request, 'Timetable slot deleted successfully!')
            except Exception as e:
                messages.error(request, f'Error deleting slot: {str(e)}')
            return redirect('timetable')
            
        else: # Add slot
            batch_id = request.POST.get('batch_id')
            teacher_id = request.POST.get('teacher_id')
            day_of_week = request.POST.get('day_of_week')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            room_number = request.POST.get('room_number')
            
            try:
                batch = Batch.objects.get(batch_id=batch_id)
                teacher = User.objects.get(user_id=teacher_id) if teacher_id else batch.teacher
                
                Timetable.objects.create(
                    batch=batch,
                    teacher=teacher,
                    day_of_week=day_of_week,
                    start_time=start_time or batch.start_time,
                    end_time=end_time or batch.end_time,
                    room_number=room_number or f"Studio {batch.batch_code or '1'}",
                    created_by=user.user_id
                )
                messages.success(request, 'Timetable slot added successfully!')
            except Exception as e:
                messages.error(request, f'Error adding slot: {str(e)}')
            return redirect('timetable')
        
    slots = Timetable.objects.select_related('batch', 'batch__course', 'teacher').filter(is_active=True).order_by('start_time')

    # Filter logic
    search = request.GET.get('search', '').strip()
    batch_filter = request.GET.get('batch_id', '').strip()
    teacher_filter = request.GET.get('teacher_id', '').strip()
    day_filter = request.GET.get('day', '').strip()
    course_filter = request.GET.get('course_id', '').strip()
    period_filter = request.GET.get('period', '').strip()

    if search:
        slots = slots.filter(
            Q(batch__batch_name__icontains=search) |
            Q(batch__batch_code__icontains=search) |
            Q(batch__course__course_name__icontains=search) |
            Q(batch__course__course_code__icontains=search) |
            Q(teacher__display_name__icontains=search) |
            Q(room_number__icontains=search)
        )
    if batch_filter:
        slots = slots.filter(batch_id=batch_filter)
    if teacher_filter:
        slots = slots.filter(teacher_id=teacher_filter)
    if day_filter:
        slots = slots.filter(day_of_week__iexact=day_filter)
    if course_filter:
        slots = slots.filter(batch__course_id=course_filter)
    if period_filter:
        try:
            p_int = int(period_filter)
            slots = slots.filter(batch__course__duration_months=p_int)
        except ValueError:
            pass

    batches = Batch.objects.select_related('course', 'teacher').filter(is_active=True).order_by('batch_name')
    teachers = User.objects.filter(role__role_name='Teacher', is_active=True).order_by('display_name')
    courses = Course.objects.filter(is_active=True).order_by('course_name')

    # Batch periods summary for display
    batch_periods_summary = []
    for b in batches:
        dur = b.course.duration_months if b.course and b.course.duration_months else 0
        if not dur and b.start_date and b.end_date:
            dur = max(1, (b.end_date - b.start_date).days // 30)
        batch_periods_summary.append({
            'batch_id': b.batch_id,
            'batch_name': b.batch_name,
            'course_name': b.course.course_name if b.course else '-',
            'duration_months': dur,
            'days': b.course.days if b.course and b.course.days else 'Scheduled',
            'start_date': b.start_date.strftime('%d %b %Y') if b.start_date else '-',
            'end_date': b.end_date.strftime('%d %b %Y') if b.end_date else '-'
        })
    available_periods = sorted(list(set(item['duration_months'] for item in batch_periods_summary if item['duration_months'])))

    # Calculate enrollment counts per batch for display
    batch_enrollments = {}
    for b in batches:
        batch_enrollments[b.batch_id] = StudentEnrollment.objects.filter(batch=b, status=1).count()

    for s in slots:
        s.enrolled_count = batch_enrollments.get(s.batch.batch_id, 0) if s.batch else 0

    from academics.models import Holiday
    from datetime import date, timedelta
    import calendar

    # Calculate week dates
    today = date.today()
    week_start_str = request.GET.get('week_start', '').strip()
    if week_start_str:
        try:
            current_monday = date.fromisoformat(week_start_str)
            current_monday = current_monday - timedelta(days=current_monday.weekday())
        except:
            current_monday = today - timedelta(days=today.weekday())
    else:
        current_monday = today - timedelta(days=today.weekday())

    prev_week_start = (current_monday - timedelta(days=7)).isoformat()
    next_week_start = (current_monday + timedelta(days=7)).isoformat()
    current_week_str = f"{current_monday.strftime('%d %b %Y')} - {(current_monday + timedelta(days=6)).strftime('%d %b %Y')}"

    # Query holidays for this week or recurring weekly
    week_dates = [current_monday + timedelta(days=i) for i in range(7)]
    week_holidays = Holiday.objects.filter(is_active=True).filter(
        Q(holiday_date__in=week_dates) | Q(is_recurring_weekly=True)
    )

    holiday_by_date = {}
    holiday_by_dayname = {}
    for h in week_holidays:
        if h.holiday_date in week_dates:
            holiday_by_date[h.holiday_date] = h
        if h.is_recurring_weekly and h.day_of_week:
            holiday_by_dayname[h.day_of_week.lower()] = h

    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    display_days = [d for d in days_order if d.lower() == day_filter.lower()] if day_filter else days_order

    schedule_data = []
    week_holiday_count = 0
    week_class_days_count = 0

    for day in display_days:
        idx = days_order.index(day)
        d_date = current_monday + timedelta(days=idx)

        # Check if holiday by date or by recurring weekly day
        holiday_obj = holiday_by_date.get(d_date) or holiday_by_dayname.get(day.lower())
        is_holiday = (holiday_obj is not None)
        if is_holiday:
            week_holiday_count += 1
            day_slots = []
        else:
            week_class_days_count += 1
            day_slots = [s for s in slots if s.day_of_week.lower() == day.lower()]

        # Decorate slots with time period & status for d_date
        for s in day_slots:
            b = s.batch
            dur = b.course.duration_months if b and b.course and b.course.duration_months else 0
            if not dur and b and b.start_date and b.end_date:
                dur = max(1, (b.end_date - b.start_date).days // 30)
            s.duration_months = dur
            s.time_period_display = f"{dur} Month{'s' if dur > 1 else ''}"
            s.period_dates_display = f"{b.start_date.strftime('%d %b %Y')} - {b.end_date.strftime('%d %b %Y')}" if b and b.start_date and b.end_date else "-"

            if b and b.start_date and d_date < b.start_date:
                s.period_status = 'upcoming'
                s.period_status_label = f"Starts {b.start_date.strftime('%d %b')}"
                s.period_status_class = "bg-blue-50 text-blue-700 border-blue-200"
            elif b and b.end_date and d_date > b.end_date:
                s.period_status = 'completed'
                s.period_status_label = f"Course Finished ({dur} Mos ended)"
                s.period_status_class = "bg-gray-100 text-gray-500 border-gray-200"
            else:
                curr_month = max(1, min(dur, ((d_date - b.start_date).days // 30) + 1)) if b and b.start_date and dur > 0 else 1
                s.period_status = 'active'
                s.period_status_label = f"Active &bull; Month {curr_month} of {dur}"
                s.period_status_class = "bg-emerald-50 text-emerald-700 border-emerald-200"

        schedule_data.append({
            'day': day,
            'date': d_date,
            'date_str': d_date.strftime('%d %b %Y'),
            'short_date': d_date.strftime('%d %b'),
            'is_today': (d_date == today),
            'is_holiday': is_holiday,
            'holiday': holiday_obj,
            'slots': day_slots,
            'slot_count': len(day_slots)
        })

    return render(request, 'website/timetable.html', {
        'user': user,
        'schedule_data': schedule_data,
        'days': days_order,
        'batches': batches,
        'teachers': teachers,
        'courses': courses,
        'selected_course': course_filter,
        'selected_batch': batch_filter,
        'selected_teacher': teacher_filter,
        'selected_day': day_filter,
        'selected_period': period_filter,
        'available_periods': available_periods,
        'batch_periods_summary': batch_periods_summary,
        'current_monday': current_monday.isoformat(),
        'prev_week_start': prev_week_start,
        'next_week_start': next_week_start,
        'current_week_str': current_week_str,
        'week_holiday_count': week_holiday_count,
        'week_class_days_count': week_class_days_count,
        'today_iso': today.isoformat(),
        'page_title': 'Class Schedule & Timetable'
    })


def get_default_holidays(year):
    fixed = [
        (f"{year}-01-01", "New Year's Day", "Public Holiday", "New Year celebration"),
        (f"{year}-01-14", "Pongal / Makar Sankranti", "Festival", "Harvest festival"),
        (f"{year}-01-26", "Republic Day", "National Holiday", "Celebration of the Constitution of India"),
        (f"{year}-04-14", "Tamil New Year / Ambedkar Jayanti", "Public Holiday", "State and national celebration"),
        (f"{year}-05-01", "May Day / Labour Day", "Public Holiday", "International Workers' Day"),
        (f"{year}-08-15", "Independence Day", "National Holiday", "Commemoration of Indian independence"),
        (f"{year}-10-02", "Gandhi Jayanti", "National Holiday", "Birth anniversary of Mahatma Gandhi"),
        (f"{year}-12-25", "Christmas", "Public Holiday", "Christmas celebration"),
    ]
    variable = {
        2026: [
            ("2026-03-03", "Holi", "Festival", "Festival of colors"),
            ("2026-03-20", "Eid-ul-Fitr", "Festival", "Islamic festival of breaking the fast"),
            ("2026-04-03", "Good Friday", "Public Holiday", "Christian holiday commemorating the crucifixion"),
            ("2026-09-04", "Krishna Janmashtami", "Festival", "Celebration of the birth of Lord Krishna"),
            ("2026-09-14", "Ganesh Chaturthi", "Festival", "Celebration of the birth of Lord Ganesha"),
            ("2026-10-20", "Ayudha Puja / Vijaya Dashami", "Festival", "Worship of tools and victory celebration"),
            ("2026-11-08", "Deepavali", "Festival", "Festival of lights"),
        ],
        2025: [
            ("2025-03-14", "Holi", "Festival", "Festival of colors"),
            ("2025-03-31", "Eid-ul-Fitr", "Festival", "Festival of breaking the fast"),
            ("2025-04-18", "Good Friday", "Public Holiday", "Christian holiday"),
            ("2025-08-16", "Krishna Janmashtami", "Festival", "Celebration of Lord Krishna"),
            ("2025-08-27", "Ganesh Chaturthi", "Festival", "Celebration of Lord Ganesha"),
            ("2025-10-02", "Dussehra", "Festival", "Victory of good over evil"),
            ("2025-10-20", "Deepavali", "Festival", "Festival of lights"),
        ],
        2027: [
            ("2027-03-22", "Holi", "Festival", "Festival of colors"),
            ("2027-03-10", "Eid-ul-Fitr", "Festival", "Islamic festival"),
            ("2027-03-26", "Good Friday", "Public Holiday", "Christian holiday"),
            ("2027-08-25", "Krishna Janmashtami", "Festival", "Celebration of Lord Krishna"),
            ("2027-09-04", "Ganesh Chaturthi", "Festival", "Celebration of Lord Ganesha"),
            ("2027-10-09", "Dussehra", "Festival", "Festival celebration"),
            ("2027-10-29", "Deepavali", "Festival", "Festival of lights"),
        ]
    }
    holidays = list(fixed)
    if year in variable:
        holidays.extend(variable[year])
    else:
        holidays.extend([
            (f"{year}-03-15", "Holi", "Festival", "Festival of colors"),
            (f"{year}-04-05", "Good Friday", "Public Holiday", "Good Friday"),
            (f"{year}-10-25", "Deepavali", "Festival", "Festival of lights"),
        ])
    return holidays


def holidays_view(request):
    if 'user_id' not in request.session:
        return redirect('login')

    try:
        user = User.objects.get(user_id=request.session['user_id'])
    except User.DoesNotExist:
        request.session.flush()
        return redirect('login')

    from academics.models import Holiday
    from django.db.models import Q
    from datetime import date, timedelta
    import calendar

    today = date.today()
    try:
        selected_year = int(request.GET.get('year', today.year))
    except (ValueError, TypeError):
        selected_year = today.year

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add_holiday':
            name = request.POST.get('holiday_name', '').strip()
            date_from_str = request.POST.get('holiday_date', '').strip()
            date_to_str = request.POST.get('end_date', '').strip()
            htype = request.POST.get('holiday_type', 'Public Holiday').strip()
            desc = request.POST.get('description', '').strip()
            is_weekly = request.POST.get('is_recurring_weekly') == '1'
            day_of_week = request.POST.get('day_of_week', '').strip()

            if not name or not date_from_str:
                messages.error(request, 'Holiday name and start date are required.')
                return redirect(f"/holidays/?year={selected_year}")

            try:
                start_dt = date.fromisoformat(date_from_str)
                end_dt = date.fromisoformat(date_to_str) if date_to_str else start_dt
                if end_dt < start_dt:
                    end_dt = start_dt

                curr = start_dt
                created_count = 0
                while curr <= end_dt:
                    d_day = curr.strftime('%A')
                    Holiday.objects.update_or_create(
                        holiday_date=curr,
                        defaults={
                            'holiday_name': name,
                            'holiday_type': htype,
                            'description': desc,
                            'is_recurring_weekly': is_weekly,
                            'day_of_week': day_of_week or d_day,
                            'is_active': True,
                            'created_by': user.user_id
                        }
                    )
                    created_count += 1
                    curr += timedelta(days=1)

                messages.success(request, f"Successfully set {created_count} holiday day(s): {name}")
            except Exception as e:
                messages.error(request, f"Error saving holiday: {str(e)}")
            return redirect(f"/holidays/?year={selected_year}")

        elif action == 'edit_holiday':
            holiday_id = request.POST.get('holiday_id')
            name = request.POST.get('holiday_name', '').strip()
            date_str = request.POST.get('holiday_date', '').strip()
            htype = request.POST.get('holiday_type', 'Public Holiday').strip()
            desc = request.POST.get('description', '').strip()
            try:
                h = Holiday.objects.get(holiday_id=holiday_id)
                h.holiday_name = name
                if date_str:
                    h.holiday_date = date.fromisoformat(date_str)
                    h.day_of_week = h.holiday_date.strftime('%A')
                h.holiday_type = htype
                h.description = desc
                h.save()
                messages.success(request, f"Holiday '{name}' updated successfully.")
            except Exception as e:
                messages.error(request, f"Error updating holiday: {str(e)}")
            return redirect(f"/holidays/?year={selected_year}")

        elif action == 'delete_holiday':
            holiday_id = request.POST.get('holiday_id')
            try:
                Holiday.objects.filter(holiday_id=holiday_id).delete()
                messages.success(request, "Holiday deleted successfully.")
            except Exception as e:
                messages.error(request, f"Error deleting holiday: {str(e)}")
            return redirect(f"/holidays/?year={selected_year}")

        elif action == 'populate_defaults':
            year = int(request.POST.get('year', selected_year))
            defaults = get_default_holidays(year)
            added = 0
            for dt_str, h_name, h_type, h_desc in defaults:
                dt = date.fromisoformat(dt_str)
                d_day = dt.strftime('%A')
                obj, created = Holiday.objects.get_or_create(
                    holiday_date=dt,
                    defaults={
                        'holiday_name': h_name,
                        'holiday_type': h_type,
                        'description': h_desc,
                        'day_of_week': d_day,
                        'is_active': True,
                        'created_by': user.user_id
                    }
                )
                if created:
                    added += 1
            messages.success(request, f"Populated {added} standard holidays for {year}!")
            return redirect(f"/holidays/?year={year}")

        elif action == 'bulk_weekly_off':
            year = int(request.POST.get('year', selected_year))
            target_day = request.POST.get('day_to_mark', 'Sunday')
            days_to_add = ['Sunday'] if target_day == 'Sunday' else (['Saturday'] if target_day == 'Saturday' else ['Saturday', 'Sunday'])

            curr = date(year, 1, 1)
            end = date(year, 12, 31)
            added = 0
            while curr <= end:
                d_name = curr.strftime('%A')
                if d_name in days_to_add:
                    obj, created = Holiday.objects.get_or_create(
                        holiday_date=curr,
                        defaults={
                            'holiday_name': f"{d_name} Weekly Off",
                            'holiday_type': 'Weekly Off',
                            'description': f"Regular weekly off ({d_name})",
                            'day_of_week': d_name,
                            'is_recurring_weekly': True,
                            'is_active': True,
                            'created_by': user.user_id
                        }
                    )
                    if created:
                        added += 1
                curr += timedelta(days=1)
            messages.success(request, f"Added {added} {target_day} weekly off days for {year}!")
            return redirect(f"/holidays/?year={year}")

        elif action == 'clear_year':
            year = int(request.POST.get('year', selected_year))
            deleted_count, _ = Holiday.objects.filter(holiday_date__year=year).delete()
            messages.success(request, f"Cleared {deleted_count} holidays for {year}.")
            return redirect(f"/holidays/?year={year}")

    holidays_qs = Holiday.objects.filter(is_active=True, holiday_date__year=selected_year).order_by('holiday_date')

    search = request.GET.get('search', '').strip()
    month_filter = request.GET.get('month', '').strip()
    type_filter = request.GET.get('type', '').strip()

    filtered_holidays = holidays_qs
    if search:
        filtered_holidays = filtered_holidays.filter(
            Q(holiday_name__icontains=search) | Q(description__icontains=search)
        )
    if month_filter:
        try:
            m_int = int(month_filter)
            filtered_holidays = filtered_holidays.filter(holiday_date__month=m_int)
        except ValueError:
            pass
    if type_filter:
        filtered_holidays = filtered_holidays.filter(holiday_type__iexact=type_filter)

    total_days_in_year = 366 if calendar.isleap(selected_year) else 365
    total_holidays_count = holidays_qs.count()
    class_days_count = max(0, total_days_in_year - total_holidays_count)
    public_holidays_count = holidays_qs.exclude(holiday_type='Weekly Off').count()
    weekly_offs_count = holidays_qs.filter(holiday_type='Weekly Off').count()

    upcoming_holidays = Holiday.objects.filter(is_active=True, holiday_date__gte=today).order_by('holiday_date')[:5]

    months_data = []
    holidays_by_date = {h.holiday_date: h for h in holidays_qs}
    for m in range(1, 13):
        m_name = calendar.month_name[m]
        _, num_days = calendar.monthrange(selected_year, m)
        m_holidays = [h for h in holidays_qs if h.holiday_date.month == m]
        days_in_m = []
        for d in range(1, num_days + 1):
            dt = date(selected_year, m, d)
            h_entry = holidays_by_date.get(dt)
            days_in_m.append({
                'day': d,
                'date': dt,
                'day_name': dt.strftime('%a'),
                'is_holiday': (h_entry is not None),
                'holiday': h_entry,
                'is_today': (dt == today)
            })
        months_data.append({
            'month_num': m,
            'month_name': m_name,
            'holidays_count': len(m_holidays),
            'class_days_count': num_days - len(m_holidays),
            'days': days_in_m
        })

    years = [selected_year - 1, selected_year, selected_year + 1, selected_year + 2]
    months_list = [(i, calendar.month_name[i]) for i in range(1, 13)]
    holiday_types = ['Public Holiday', 'National Holiday', 'Festival', 'Academy Off', 'Weekly Off', 'Emergency']

    return render(request, 'website/holidays.html', {
        'user': user,
        'holidays': filtered_holidays,
        'all_year_holidays': holidays_qs,
        'selected_year': selected_year,
        'years': years,
        'months_list': months_list,
        'selected_month': month_filter,
        'selected_type': type_filter,
        'search': search,
        'holiday_types': holiday_types,
        'total_holidays_count': total_holidays_count,
        'class_days_count': class_days_count,
        'public_holidays_count': public_holidays_count,
        'weekly_offs_count': weekly_offs_count,
        'total_days_in_year': total_days_in_year,
        'upcoming_holidays': upcoming_holidays,
        'months_data': months_data,
        'page_title': 'Holiday Management'
    })



def get_security_settings():
    import json, os
    from django.conf import settings
    sec = {
        'phone_length': 10,
        'email_length': 255,
        'password_expire': 90,
        'attendance_from_date': '2026-09-05',
        'attendance_to_date': '2026-10-05',
    }
    try:
        path = os.path.join(settings.BASE_DIR, 'security_settings.json')
        if os.path.exists(path):
            with open(path, 'r') as fh:
                sec.update(json.load(fh))
    except Exception:
        pass
    return sec

def get_attendance_period_for_date(req_date, cfg_from, cfg_to):
    import calendar
    from datetime import date
    
    if not cfg_from or not cfg_to:
        return None, None, ""
        
    if cfg_from <= req_date <= cfg_to:
        return cfg_from, cfg_to, cfg_from.strftime('%B %Y')
        
    from_day = cfg_from.day
    to_day = cfg_to.day
    
    if from_day == to_day:
        if req_date.day >= from_day:
            p_start_year = req_date.year
            p_start_month = req_date.month
        else:
            if req_date.month == 1:
                p_start_year = req_date.year - 1
                p_start_month = 12
            else:
                p_start_year = req_date.year
                p_start_month = req_date.month - 1
                
        if p_start_month == 12:
            p_end_year = p_start_year + 1
            p_end_month = 1
        else:
            p_end_year = p_start_year
            p_end_month = p_start_month + 1
            
        max_s_day = calendar.monthrange(p_start_year, p_start_month)[1]
        max_e_day = calendar.monthrange(p_end_year, p_end_month)[1]
        p_start = date(p_start_year, p_start_month, min(from_day, max_s_day))
        p_end = date(p_end_year, p_end_month, min(to_day, max_e_day))
        p_name = p_start.strftime('%B %Y')
        return p_start, p_end, p_name
        
    return cfg_from, cfg_to, ""

def validate_attendance_date_range(from_date_str, to_date_str=None, current_date=None):
    from datetime import datetime, date
    sec = get_security_settings()
    allowed_from_str = sec.get('attendance_from_date')
    allowed_to_str = sec.get('attendance_to_date')

    def parse_d(val):
        if not val:
            return None
        if isinstance(val, date):
            return val
        for fmt in ('%Y-%m-%d', '%d-%m-%Y', '%d/%m/%Y'):
            try:
                return datetime.strptime(str(val).strip(), fmt).date()
            except (ValueError, TypeError):
                pass
        return None

    cfg_from = parse_d(allowed_from_str)
    cfg_to = parse_d(allowed_to_str)
    req_from = parse_d(from_date_str)
    req_to = parse_d(to_date_str) if to_date_str else req_from
    today = current_date or date.today()

    if not cfg_from or not cfg_to:
        return True, ""

    if not req_from:
        return False, "Please provide a valid attendance date."

    # Validate each date against its respective attendance period cutoff
    for d in (req_from, req_to):
        p_start, p_end, p_name = get_attendance_period_for_date(d, cfg_from, cfg_to)
        if p_end:
            if today > p_end:
                period_label = f"{p_name} " if p_name else ""
                end_str = p_end.strftime('%d-%m-%Y')
                return False, f"The {period_label}attendance period ended on {end_str}. Once the period end date has passed, new attendance requests cannot be applied for this period."

    return True, ""


def student_attendance_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    from users.models import User
    try:

        user = User.objects.get(user_id=request.session['user_id'])

    except User.DoesNotExist:

        request.session.flush()

        return redirect('login')
    from academics.models import Batch, StudentAttendance, StudentAttendanceDetail
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action in ('mark_attendance', 'apply_leave'):
            from_date = request.POST.get('from_date') or request.POST.get('attendance_date')
            to_date = request.POST.get('to_date') or from_date
            is_valid, err_msg = validate_attendance_date_range(from_date, to_date)
            if not is_valid:
                messages.error(request, err_msg)
                return redirect('student_attendance')
            batch_id = request.POST.get('batch_id')
            student_id = request.POST.get('student_id')
            status = request.POST.get('status')
            if not status and request.POST.get('request_type'):
                rt = request.POST.get('request_type').strip().lower()
                status_map = {'present': 1, 'absent': 2, 'late': 3, 'leave': 4, 'on duty': 5, 'permission': 6, 'work from home': 7}
                status = status_map.get(rt, 4)
            approval_status = 'Pending'
            status_labels = {1: 'Present', 2: 'Absent', 3: 'Late', 4: 'Leave', 5: 'On Duty', 6: 'Permission', 7: 'Work From Home'}
            status_label = status_labels.get(int(status) if status else 1, 'Leave')
            remarks = request.POST.get('remarks') or request.POST.get('request_type', '')
            
            batch = Batch.objects.filter(batch_id=batch_id).first() if batch_id else None
            student = User.objects.filter(user_id=student_id).first() if student_id else None
            
            if from_date and student:
                from datetime import datetime, timedelta
                d_from = datetime.strptime(str(from_date).strip(), '%Y-%m-%d').date()
                d_to = datetime.strptime(str(to_date).strip(), '%Y-%m-%d').date() if to_date else d_from
                course = batch.course if batch else None
                cur = d_from
                count = 0
                while cur <= d_to:
                    att_record, _ = StudentAttendance.objects.get_or_create(
                        attendance_date=cur,
                        batch=batch,
                        defaults={'course': course, 'created_by': user.user_id}
                    )
                    StudentAttendanceDetail.objects.update_or_create(
                        student_attendance=att_record,
                        student=student,
                        defaults={
                            'attendance_status': int(status) if status else 1,
                            'approval_status': 'Pending',
                            'remarks': remarks,
                            'created_by': user.user_id
                        }
                    )
                    cur += timedelta(days=1)
                    count += 1

                from academics.models import LeaveRequest
                LeaveRequest.objects.create(
                    user=student,
                    user_type='Student',
                    from_date=d_from,
                    to_date=d_to,
                    no_of_days=count,
                    request_type=status_label,
                    manager_approval_status='Pending',
                    batch=batch,
                    created_by=user.user_id
                )
                messages.success(request, f'Attendance marked for {student.display_name or student.first_name} ({count} day{"s" if count > 1 else ""})! Status: Pending Approval.')
            return redirect('student_attendance')
        elif action in ('approve_attendance', 'reject_attendance'):
            detail_id = request.POST.get('detail_id')
            if detail_id:
                new_app = 'Approved' if action == 'approve_attendance' else 'Rejected'
                detail = StudentAttendanceDetail.objects.filter(student_attendance_detail_id=detail_id).first()
                if detail:
                    detail.approval_status = new_app
                    detail.save()
                    from academics.models import LeaveRequest
                    from django.utils import timezone
                    LeaveRequest.objects.filter(
                        user=detail.student,
                        from_date__lte=detail.student_attendance.attendance_date,
                        to_date__gte=detail.student_attendance.attendance_date
                    ).update(manager_approval_status=new_app, manager_approval_on=timezone.now())
                messages.success(request, f'Attendance {new_app.lower()} successfully!')
            return redirect('student_attendance')
        elif action == 'update_attendance':
            detail_id = request.POST.get('detail_id')
            status = request.POST.get('status')
            approval_status = request.POST.get('approval_status')
            remarks = (request.POST.get('remarks') or '').strip()
            if detail_id:
                detail = StudentAttendanceDetail.objects.filter(student_attendance_detail_id=detail_id).first()
                if detail:
                    if detail.approval_status != 'Pending':
                        messages.error(request, f'Cannot update attendance record that has already been {detail.approval_status.lower()}. Only pending records can be updated.')
                        return redirect('student_attendance')
                    if status:
                        try:
                            detail.attendance_status = int(status)
                        except (ValueError, TypeError):
                            pass
                    if approval_status in ('Pending', 'Approved', 'Rejected'):
                        detail.approval_status = approval_status
                    detail.remarks = remarks
                    detail.save()
                    
                    from academics.models import LeaveRequest
                    from django.utils import timezone
                    lr_status = approval_status if approval_status in ('Approved', 'Rejected') else 'Pending'
                    LeaveRequest.objects.filter(
                        user=detail.student,
                        from_date__lte=detail.student_attendance.attendance_date,
                        to_date__gte=detail.student_attendance.attendance_date
                    ).update(
                        manager_approval_status=lr_status,
                        manager_approval_on=timezone.now() if lr_status != 'Pending' else None
                    )
                    messages.success(request, 'Attendance details updated successfully!')
            return redirect('student_attendance')
        elif action == 'delete_attendance':
            detail_id = request.POST.get('detail_id')
            if detail_id:
                detail = StudentAttendanceDetail.objects.filter(student_attendance_detail_id=detail_id).first()
                if detail:
                    if detail.approval_status != 'Pending':
                        messages.error(request, f'Cannot delete attendance record that has already been {detail.approval_status.lower()}. Only pending records can be deleted.')
                        return redirect('student_attendance')
                    detail.delete()
                    messages.success(request, 'Attendance record deleted successfully!')
            return redirect('student_attendance')
            
    # Filters
    from academics.models import StudentEnrollment
    allocated_batches = [e.batch for e in StudentEnrollment.objects.filter(student=user, status=1, batch__isnull=False).select_related('batch')]
    
    selected_batch = request.GET.get('batch_id', '')
    selected_student = request.GET.get('student_id', '')
    selected_date = request.GET.get('date', '')
    selected_approval_status = request.GET.get('approval_status', '')
    
    batches = Batch.objects.filter(is_active=True)
    students = User.objects.filter(role__role_name__iexact='student', is_active=True)
    
    # Query Daily Attendance records
    details = StudentAttendanceDetail.objects.select_related(
        'student', 'student_attendance', 'student_attendance__batch', 'student_attendance__course', 'student_attendance__batch__course'
    ).order_by('-student_attendance__attendance_date', '-student_attendance_detail_id')
    
    if selected_batch:
        details = details.filter(student_attendance__batch_id=selected_batch)
    if selected_student:
        details = details.filter(student_id=selected_student)
    if selected_date:
        details = details.filter(student_attendance__attendance_date=selected_date)
    if selected_approval_status:
        details = details.filter(approval_status=selected_approval_status)

    return render(request, 'website/student_attendance.html', {
        'user': user,
        'page_title': 'Student Attendance',
        'batches': batches,
        'students': students,
        'details': details,
        'selected_batch': selected_batch,
        'selected_student': selected_student,
        'selected_date': selected_date,
        'selected_approval_status': selected_approval_status,
        'allocated_batches': allocated_batches
    })

def teacher_attendance_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    from users.models import User
    try:

        user = User.objects.get(user_id=request.session['user_id'])

    except User.DoesNotExist:

        request.session.flush()

        return redirect('login')
    from academics.models import TeacherAttendance, TeacherAttendanceDetail
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action in ('mark_teacher_attendance', 'apply_leave'):
            from_date = request.POST.get('from_date') or request.POST.get('attendance_date')
            to_date = request.POST.get('to_date') or from_date
            is_valid, err_msg = validate_attendance_date_range(from_date, to_date)
            if not is_valid:
                messages.error(request, err_msg)
                return redirect('teacher_attendance')
            teacher_id = request.POST.get('teacher_id')
            status = request.POST.get('status')
            if not status and request.POST.get('request_type'):
                rt = request.POST.get('request_type').strip().lower()
                status_map = {'present': 1, 'absent': 2, 'late': 3, 'leave': 4, 'on duty': 5, 'permission': 6, 'work from home': 7}
                status = status_map.get(rt, 4)
            approval_status = 'Pending'
            status_labels = {1: 'Present', 2: 'Absent', 3: 'Late', 4: 'Leave', 5: 'On Duty', 6: 'Permission', 7: 'Work From Home'}
            status_label = status_labels.get(int(status) if status else 1, 'Leave')
            check_in_time = request.POST.get('check_in_time') or None
            check_out_time = request.POST.get('check_out_time') or None
            remarks = request.POST.get('remarks') or request.POST.get('request_type', '')
            teacher = User.objects.filter(user_id=teacher_id).first() if teacher_id else None
            if from_date and teacher:
                from datetime import datetime, timedelta
                d_from = datetime.strptime(str(from_date).strip(), '%Y-%m-%d').date()
                d_to = datetime.strptime(str(to_date).strip(), '%Y-%m-%d').date() if to_date else d_from
                cur = d_from
                count = 0
                while cur <= d_to:
                    att_record, _ = TeacherAttendance.objects.get_or_create(
                        attendance_date=cur,
                        defaults={'created_by': user.user_id}
                    )
                    TeacherAttendanceDetail.objects.update_or_create(
                        teacher_attendance=att_record,
                        teacher=teacher,
                        defaults={
                            'attendance_status': int(status) if status else 1,
                            'approval_status': 'Pending',
                            'check_in_time': check_in_time,
                            'check_out_time': check_out_time,
                            'remarks': remarks,
                            'created_by': user.user_id
                        }
                    )
                    cur += timedelta(days=1)
                    count += 1

                from academics.models import LeaveRequest
                LeaveRequest.objects.create(
                    user=teacher,
                    user_type='Teacher',
                    from_date=d_from,
                    to_date=d_to,
                    no_of_days=count,
                    request_type=status_label,
                    manager_approval_status='Pending',
                    created_by=user.user_id
                )
                messages.success(request, f'Attendance marked for {teacher.display_name or teacher.first_name} ({count} day{"s" if count > 1 else ""})! Status: Pending Approval.')
            return redirect('teacher_attendance')
        elif action in ('approve_teacher_attendance', 'reject_teacher_attendance'):
            detail_id = request.POST.get('detail_id')
            if detail_id:
                new_app = 'Approved' if action == 'approve_teacher_attendance' else 'Rejected'
                detail = TeacherAttendanceDetail.objects.filter(teacher_attendance_detail_id=detail_id).first()
                if detail:
                    detail.approval_status = new_app
                    detail.save()
                    from academics.models import LeaveRequest
                    from django.utils import timezone
                    LeaveRequest.objects.filter(
                        user=detail.teacher,
                        from_date__lte=detail.teacher_attendance.attendance_date,
                        to_date__gte=detail.teacher_attendance.attendance_date
                    ).update(manager_approval_status=new_app, manager_approval_on=timezone.now())
                messages.success(request, f'Teacher attendance {new_app.lower()} successfully!')
            return redirect('teacher_attendance')
        elif action == 'update_teacher_attendance':
            detail_id = request.POST.get('detail_id')
            if detail_id:
                detail = TeacherAttendanceDetail.objects.filter(teacher_attendance_detail_id=detail_id).first()
                if detail:
                    if detail.approval_status != 'Pending':
                        messages.error(request, f'Cannot update attendance that has already been {detail.approval_status.lower()}. Only pending records can be updated.')
                        return redirect('teacher_attendance')
                    status = request.POST.get('status')
                    if status:
                        try:
                            detail.attendance_status = int(status)
                        except (ValueError, TypeError):
                            pass
                    approval_status = request.POST.get('approval_status')
                    if approval_status in ('Pending', 'Approved', 'Rejected'):
                        detail.approval_status = approval_status
                    check_in = request.POST.get('check_in_time')
                    check_out = request.POST.get('check_out_time')
                    detail.check_in_time = check_in if check_in else None
                    detail.check_out_time = check_out if check_out else None
                    detail.remarks = (request.POST.get('remarks') or '').strip()
                    detail.save()
                    
                    from academics.models import LeaveRequest
                    from django.utils import timezone
                    lr_status = detail.approval_status if detail.approval_status in ('Approved', 'Rejected') else 'Pending'
                    LeaveRequest.objects.filter(
                        user=detail.teacher,
                        from_date__lte=detail.teacher_attendance.attendance_date,
                        to_date__gte=detail.teacher_attendance.attendance_date
                    ).update(
                        manager_approval_status=lr_status,
                        manager_approval_on=timezone.now() if lr_status != 'Pending' else None
                    )
                    messages.success(request, 'Teacher attendance updated successfully!')
            return redirect('teacher_attendance')
        elif action == 'delete_teacher_attendance':
            detail_id = request.POST.get('detail_id')
            if detail_id:
                detail = TeacherAttendanceDetail.objects.filter(teacher_attendance_detail_id=detail_id).first()
                if detail:
                    if detail.approval_status != 'Pending':
                        messages.error(request, f'Cannot delete attendance record that has already been {detail.approval_status.lower()}. Only pending records can be deleted.')
                        return redirect('teacher_attendance')
                    detail.delete()
                    messages.success(request, 'Attendance record deleted successfully!')
            return redirect('teacher_attendance')
            
    # Filters
    from academics.models import Batch
    allocated_batches = list(Batch.objects.filter(teacher=user, is_active=True))
    
    selected_teacher = request.GET.get('teacher_id', '')
    selected_date = request.GET.get('date', '')
    selected_approval_status = request.GET.get('approval_status', '')
    
    teachers = User.objects.filter(role__role_name__iexact='teacher', is_active=True)
    
    details = TeacherAttendanceDetail.objects.select_related('teacher_attendance', 'teacher').order_by('-teacher_attendance__attendance_date')
    
    if selected_teacher:
        details = details.filter(teacher_id=selected_teacher)
        
    if selected_date:
        details = details.filter(teacher_attendance__attendance_date=selected_date)

    if selected_approval_status:
        details = details.filter(approval_status=selected_approval_status)

    return render(request, 'website/teacher_attendance.html', {
        'user': user,
        'page_title': 'Teacher Attendance',
        'teachers': teachers,
        'details': details,
        'selected_teacher': selected_teacher,
        'selected_date': selected_date,
        'selected_approval_status': selected_approval_status,
        'allocated_batches': allocated_batches
    })


def sync_enrollment_fees(created_by_id=None):
    try:
        from academics.models import StudentEnrollment
        from finance.models import StudentFee
        for enrollment in StudentEnrollment.objects.select_related('student', 'course', 'batch').all():
            if enrollment.course and enrollment.student:
                fee_amt = enrollment.course.fee_amount or 0
                sf, created = StudentFee.objects.get_or_create(
                    student=enrollment.student,
                    course=enrollment.course,
                    defaults={
                        'batch': enrollment.batch,
                        'total_amount': fee_amt,
                        'discount_amount': 0,
                        'final_amount': fee_amt,
                        'due_date': (enrollment.batch.end_date if enrollment.batch else None) or (enrollment.batch.start_date if enrollment.batch else None),
                        'status': 1,
                        'created_by': created_by_id
                    }
                )
                if not created and sf.batch != enrollment.batch:
                    sf.batch = enrollment.batch
                    sf.save()
    except Exception as e:
        print(f"Error in sync_enrollment_fees: {e}")


def fee_dashboard_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    try:
        user = User.objects.get(user_id=request.session['user_id'])
    except User.DoesNotExist:
        request.session.flush()
        return redirect('login')
    
    import json
    from datetime import date
    from django.utils import timezone
    from django.db.models import Sum, F
    from finance.models import StudentFee, FeePayment, FeeReceipt

    sync_enrollment_fees(user.user_id)

    today = timezone.now().date()
    today_str = today.strftime('%d-%m-%Y')

    # Query real database payments
    today_payments_qs = FeePayment.objects.filter(payment_date__date=today).select_related('student_fee', 'student_fee__student', 'student_fee__course', 'student_fee__batch')
    todays_sum = today_payments_qs.aggregate(total=Sum('paid_amount'))['total'] or 0
    todays_collection = f"{todays_sum:,.2f}" if todays_sum > 0 else "0.00"

    monthly_payments_qs = FeePayment.objects.filter(
        payment_date__year=today.year,
        payment_date__month=today.month
    ).select_related('student_fee', 'student_fee__student', 'student_fee__course', 'student_fee__batch')
    monthly_sum = monthly_payments_qs.aggregate(total=Sum('paid_amount'))['total'] or 0
    monthly_collection = f"{monthly_sum:,.2f}" if monthly_sum > 0 else "0.00"

    # Query real database fees
    all_fees = StudentFee.objects.all().select_related('student', 'course', 'batch')
    pending_fees_qs = all_fees.filter(status__in=[1, 2])
    pending_sum = pending_fees_qs.aggregate(total=Sum('final_amount'))['total'] or 0
    pending_fees = f"{pending_sum:,.2f}" if pending_sum > 0 else "0.00"

    overdue_fees_qs = all_fees.filter(status__in=[1, 2], due_date__lt=today)
    overdue_sum = overdue_fees_qs.aggregate(total=Sum('final_amount'))['total'] or 0
    overdue_fees = f"{overdue_sum:,.2f}" if overdue_sum > 0 else "0.00"

    students_paid_count = all_fees.filter(status=3).values('student').distinct().count()
    students_pending_count = all_fees.filter(status__in=[1, 2]).values('student').distinct().count()

    payment_mode_map = {1: 'Cash', 2: 'UPI', 3: 'Credit Card', 4: 'Debit Card', 5: 'Net Banking'}

    # Build real details lists from database only
    todays_details = []
    for p in today_payments_qs.order_by('-payment_date'):
        stu = p.student_fee.student if p.student_fee else None
        todays_details.append({
            'receipt_no': p.receipt_no or f"RCP-{p.fee_payment_id:04d}",
            'student_id': stu.user_id if stu else '',
            'student_name': stu.display_name or f"{stu.first_name} {stu.last_name}".strip() if stu else '-',
            'phone': stu.phone if stu else '-',
            'email': stu.email if stu else '-',
            'course': p.student_fee.course.course_name if p.student_fee and p.student_fee.course else '-',
            'batch': p.student_fee.batch.batch_name if p.student_fee and p.student_fee.batch else '-',
            'amount': f"{p.paid_amount:,.2f}",
            'mode': payment_mode_map.get(p.payment_mode, 'Other'),
            'txn_id': p.transaction_no or '-',
            'time': p.payment_date.strftime('%I:%M %p') if p.payment_date else '-',
            'date': p.payment_date.strftime('%d-%m-%Y') if p.payment_date else today_str,
            'status': 'Completed'
        })

    monthly_details = []
    for p in monthly_payments_qs.order_by('-payment_date'):
        stu = p.student_fee.student if p.student_fee else None
        monthly_details.append({
            'receipt_no': p.receipt_no or f"RCP-{p.fee_payment_id:04d}",
            'student_id': stu.user_id if stu else '',
            'student_name': stu.display_name or f"{stu.first_name} {stu.last_name}".strip() if stu else '-',
            'phone': stu.phone if stu else '-',
            'email': stu.email if stu else '-',
            'course': p.student_fee.course.course_name if p.student_fee and p.student_fee.course else '-',
            'batch': p.student_fee.batch.batch_name if p.student_fee and p.student_fee.batch else '-',
            'amount': f"{p.paid_amount:,.2f}",
            'mode': payment_mode_map.get(p.payment_mode, 'Other'),
            'txn_id': p.transaction_no or '-',
            'date': p.payment_date.strftime('%d-%m-%Y') if p.payment_date else '-',
            'status': 'Completed'
        })

    pending_details = []
    for sf in pending_fees_qs.order_by('due_date'):
        stu = sf.student
        paid_amt = FeePayment.objects.filter(student_fee=sf).aggregate(total=Sum('paid_amount'))['total'] or 0
        pend_amt = max(0, sf.final_amount - paid_amt)
        is_overdue = sf.due_date and sf.due_date < today
        pending_details.append({
            'student_id': stu.user_id if stu else '',
            'student_name': stu.display_name or f"{stu.first_name} {stu.last_name}".strip() if stu else '-',
            'phone': stu.phone if stu else '-',
            'email': stu.email if stu else '-',
            'course': sf.course.course_name if sf.course else '-',
            'batch': sf.batch.batch_name if sf.batch else '-',
            'total_fee': f"{sf.final_amount:,.2f}",
            'paid_amount': f"{paid_amt:,.2f}",
            'pending_amount': f"{pend_amt:,.2f}",
            'due_date': sf.due_date.strftime('%d-%m-%Y') if sf.due_date else '-',
            'status': 'Overdue' if is_overdue else 'Pending'
        })

    overdue_details = []
    for sf in overdue_fees_qs.order_by('due_date'):
        stu = sf.student
        paid_amt = FeePayment.objects.filter(student_fee=sf).aggregate(total=Sum('paid_amount'))['total'] or 0
        pend_amt = max(0, sf.final_amount - paid_amt)
        days_ovd = (today - sf.due_date).days if sf.due_date else 0
        overdue_details.append({
            'student_id': stu.user_id if stu else '',
            'student_name': stu.display_name or f"{stu.first_name} {stu.last_name}".strip() if stu else '-',
            'phone': stu.phone if stu else '-',
            'email': stu.email if stu else '-',
            'course': sf.course.course_name if sf.course else '-',
            'batch': sf.batch.batch_name if sf.batch else '-',
            'total_fee': f"{sf.final_amount:,.2f}",
            'paid_amount': f"{paid_amt:,.2f}",
            'overdue_amount': f"{pend_amt:,.2f}",
            'due_date': sf.due_date.strftime('%d-%m-%Y') if sf.due_date else '-',
            'days_overdue': days_ovd,
            'status': 'Overdue'
        })

    students_paid_details = []
    for sf in all_fees.filter(status=3).order_by('-created_date'):
        stu = sf.student
        last_payment = FeePayment.objects.filter(student_fee=sf).order_by('-payment_date').first()
        students_paid_details.append({
            'student_id': stu.user_id if stu else '',
            'student_name': stu.display_name or f"{stu.first_name} {stu.last_name}".strip() if stu else '-',
            'phone': stu.phone if stu else '-',
            'email': stu.email if stu else '-',
            'course': sf.course.course_name if sf.course else '-',
            'batch': sf.batch.batch_name if sf.batch else '-',
            'total_fee': f"{sf.final_amount:,.2f}",
            'paid_amount': f"{sf.final_amount:,.2f}",
            'receipt_no': last_payment.receipt_no if last_payment and last_payment.receipt_no else '-',
            'payment_date': last_payment.payment_date.strftime('%d-%m-%Y') if last_payment and last_payment.payment_date else '-',
            'status': 'Fully Paid'
        })

    students_pending_details = pending_details

    context = {
        'user': user,
        'page_title': 'Fee Dashboard',
        'todays_collection': todays_collection,
        'monthly_collection': monthly_collection,
        'pending_fees': pending_fees,
        'overdue_fees': overdue_fees,
        'students_paid': str(students_paid_count),
        'students_pending': str(students_pending_count),
        'todays_details_json': json.dumps(todays_details),
        'monthly_details_json': json.dumps(monthly_details),
        'pending_details_json': json.dumps(pending_details),
        'overdue_details_json': json.dumps(overdue_details),
        'students_paid_details_json': json.dumps(students_paid_details),
        'students_pending_details_json': json.dumps(students_pending_details),
    }
    return render(request, 'website/fee_dashboard.html', context)


def fee_collection_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    try:
        user = User.objects.get(user_id=request.session['user_id'])
    except User.DoesNotExist:
        request.session.flush()
        return redirect('login')
    
    from academics.models import Course, Batch
    from finance.models import FeePayment, StudentFee, FeeReceipt
    from django.db.models import Sum
    from django.utils import timezone
    import random
    from decimal import Decimal
    
    sync_enrollment_fees(user.user_id)
    
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        course_id = request.POST.get('course_id')
        batch_id = request.POST.get('batch_id')
        payment_mode = request.POST.get('payment_mode') or 2
        transaction_no = request.POST.get('transaction_no') or ''
        amount_paid_str = request.POST.get('amount_paid') or '0'
        
        try:
            paid_amt = Decimal(str(amount_paid_str).strip() or '0')
            student = User.objects.get(user_id=student_id)
            course = Course.objects.filter(course_id=course_id).first() if course_id else None
            batch = Batch.objects.filter(batch_id=batch_id).first() if batch_id else None
            
            sf = StudentFee.objects.filter(student=student, course=course).order_by('-student_fee_id').first()
            if not sf:
                fee_amt = course.fee_amount if (course and course.fee_amount) else paid_amt
                sf = StudentFee.objects.create(
                    student=student,
                    course=course,
                    batch=batch,
                    total_amount=fee_amt,
                    discount_amount=0,
                    final_amount=fee_amt,
                    due_date=batch.end_date if batch else None,
                    status=1,
                    created_by=user.user_id
                )
            elif batch and not sf.batch:
                sf.batch = batch
                sf.save()
                
            receipt_num = f"RCP-{timezone.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
            
            fp = FeePayment.objects.create(
                student_fee=sf,
                receipt_no=receipt_num,
                paid_amount=paid_amt,
                payment_mode=int(payment_mode),
                transaction_no=transaction_no,
                remarks='Fee collected via web portal',
                created_by=user.user_id
            )
            
            FeeReceipt.objects.create(
                receipt_no=receipt_num,
                student=student,
                fee_payment=fp,
                total_amount=paid_amt,
                generated_by=user.user_id
            )
            
            total_paid = FeePayment.objects.filter(student_fee=sf).aggregate(total=Sum('paid_amount'))['total'] or 0
            if total_paid >= sf.final_amount:
                sf.status = 3
            elif total_paid > 0:
                sf.status = 2
            else:
                sf.status = 1
            sf.save()
            
            messages.success(request, f'Fee payment of ₹{paid_amt:,.2f} collected successfully! Receipt {receipt_num} generated.')
            return redirect('fee_collection')
        except Exception as e:
            messages.error(request, f'Error collecting fee: {str(e)}')
            return redirect('fee_collection')
            
    students = User.objects.filter(role__role_name='Student', is_active=True).order_by('first_name', 'last_name')
    courses = Course.objects.filter(is_active=True).order_by('course_name')
    batches = Batch.objects.filter(is_active=True).order_by('batch_name')
    
    selected_student_id = request.GET.get('student_id', '')
    selected_student_name = request.GET.get('student', '')
    if not selected_student_id and selected_student_name:
        st_match = students.filter(display_name__iexact=selected_student_name).first() or \
                   students.filter(first_name__iexact=selected_student_name).first()
        if st_match:
            selected_student_id = str(st_match.user_id)
            
    payment_mode_map = {1: 'Cash', 2: 'UPI', 3: 'Credit Card', 4: 'Debit Card', 5: 'Net Banking'}
    recent_payments = FeePayment.objects.select_related(
        'student_fee', 'student_fee__student', 'student_fee__course', 'student_fee__batch'
    ).order_by('-payment_date')[:20]
    
    formatted_payments = []
    for p in recent_payments:
        stu = p.student_fee.student if p.student_fee else None
        formatted_payments.append({
            'receipt_no': p.receipt_no or f"RCP-{p.fee_payment_id:04d}",
            'date': p.payment_date.strftime('%d/%m/%Y') if p.payment_date else '-',
            'student_name': stu.display_name or f"{stu.first_name} {stu.last_name}".strip() if stu else '-',
            'amount': f"{p.paid_amount:,.2f}",
            'mode': payment_mode_map.get(p.payment_mode, 'Other'),
            'status': 'Paid' if (p.student_fee and p.student_fee.status == 3) else 'Partial'
        })
        
    return render(request, 'website/fee_collection.html', {
        'user': user,
        'page_title': 'Fee Collection',
        'students': students,
        'courses': courses,
        'batches': batches,
        'recent_payments': formatted_payments,
        'selected_student_id': selected_student_id,
    })


# =====================================================================
# TIME & SCHEDULE CONFLICT HELPERS FOR TEACHERS AND STUDENTS
# =====================================================================
from datetime import datetime, date, time

def parse_time_val(val):
    if not val:
        return None
    if isinstance(val, time):
        return val
    val_str = str(val).strip()
    for fmt in ('%H:%M:%S', '%H:%M', '%I:%M %p', '%I:%M%p'):
        try:
            return datetime.strptime(val_str, fmt).time()
        except ValueError:
            pass
    return None

def parse_date_val(val):
    if not val:
        return None
    if isinstance(val, date):
        return val
    val_str = str(val).strip()
    for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%Y/%m/%d'):
        try:
            return datetime.strptime(val_str, fmt).date()
        except ValueError:
            pass
    return None

def times_overlap(s1, e1, s2, e2):
    t_s1 = parse_time_val(s1)
    t_e1 = parse_time_val(e1)
    t_s2 = parse_time_val(s2)
    t_e2 = parse_time_val(e2)
    if not t_s1 or not t_e1 or not t_s2 or not t_e2:
        return False
    if t_s1 == t_s2 and t_e1 == t_e2:
        return True
    # Strict inequality ensures back-to-back classes are allowed (e.g. 9:00-11:00 and 11:00-13:00)
    return (t_s1 < t_e2) and (t_e1 > t_s2)

def dates_overlap(sd1, ed1, sd2, ed2):
    d_sd1 = parse_date_val(sd1)
    d_ed1 = parse_date_val(ed1)
    d_sd2 = parse_date_val(sd2)
    d_ed2 = parse_date_val(ed2)

    if d_ed1 and d_sd2 and d_ed1 < d_sd2:
        return False
    if d_ed2 and d_sd1 and d_ed2 < d_sd1:
        return False
    return True

DAY_NAMES = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def parse_course_days(days_str):
    if not days_str:
        return set(DAY_NAMES)
    s = str(days_str).lower()
    if 'everyday' in s or 'all' in s or 'daily' in s:
        return set(DAY_NAMES)
    if 'monday to saturday' in s or 'mon to sat' in s:
        return {'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'}
    if 'monday to friday' in s or 'weekdays' in s:
        return {'monday', 'tuesday', 'wednesday', 'thursday', 'friday'}
    if 'weekend' in s:
        return {'saturday', 'sunday'}
    found = set()
    for d in DAY_NAMES:
        if d in s or d[:3] in s:
            found.add(d)
    return found if found else set(DAY_NAMES)

def check_days_overlap(course1, course2):
    if not course1 or not course2:
        return True
    days1 = parse_course_days(getattr(course1, 'days', ''))
    days2 = parse_course_days(getattr(course2, 'days', ''))
    return bool(days1.intersection(days2))

def check_teacher_time_conflict(teacher_id, start_time, end_time, start_date=None, end_date=None, course=None, exclude_batch_id=None):
    """
    Checks if teacher is already assigned to another active batch with overlapping time.
    Returns (conflicting_batch, error_message) or (None, None).
    """
    from academics.models import Batch
    from users.models import User

    if not teacher_id or not start_time or not end_time:
        return None, None

    t_s = parse_time_val(start_time)
    t_e = parse_time_val(end_time)
    if not t_s or not t_e:
        return None, None

    batches = Batch.objects.filter(
        teacher_id=teacher_id,
        is_active=True
    ).exclude(start_time__isnull=True).exclude(end_time__isnull=True).select_related('course', 'teacher')

    if exclude_batch_id:
        try:
            exclude_batch_id = int(exclude_batch_id)
            batches = batches.exclude(batch_id=exclude_batch_id)
        except (ValueError, TypeError):
            pass

    d_sd = parse_date_val(start_date)
    d_ed = parse_date_val(end_date)

    for b in batches:
        if times_overlap(t_s, t_e, b.start_time, b.end_time):
            if dates_overlap(start_date, end_date, b.start_date, b.end_date):
                exact_same_slot = (
                    t_s == b.start_time and
                    t_e == b.end_time and
                    (not d_sd or not b.start_date or d_sd == b.start_date) and
                    (not d_ed or not b.end_date or d_ed == b.end_date)
                )
                if exact_same_slot or check_days_overlap(course, b.course):
                    t_str = f"{b.start_time.strftime('%I:%M %p')} - {b.end_time.strftime('%I:%M %p')}"
                    d_str = ""
                    if b.start_date and b.end_date:
                        d_str = f", {b.start_date.strftime('%d/%m/%Y')} to {b.end_date.strftime('%d/%m/%Y')}"
                    elif b.start_date:
                        d_str = f", from {b.start_date.strftime('%d/%m/%Y')}"
                    teacher_name = b.teacher.display_name if b.teacher else "This teacher"
                    c_name = b.course.course_name if b.course else ""
                    msg = f"Teacher {teacher_name} is already assigned to batch '{b.batch_name}' ({c_name}, {t_str}{d_str}). A teacher cannot be assigned to multiple batches with the same or overlapping schedule."
                    return b, msg
    return None, None

def check_student_time_conflict(student_id, target_batch, exclude_enrollment_id=None):
    """
    Checks if student is already enrolled in another active batch with overlapping time.
    Returns (conflicting_batch, error_message) or (None, None).
    """
    from academics.models import Batch, StudentEnrollment
    from users.models import User

    if not student_id or not target_batch:
        return None, None

    if not isinstance(target_batch, Batch):
        target_batch = Batch.objects.filter(batch_id=target_batch).select_related('course').first()

    if not target_batch or not target_batch.start_time or not target_batch.end_time:
        return None, None

    enrollments = StudentEnrollment.objects.filter(
        student_id=student_id,
        status=1,
        batch__isnull=False,
        batch__is_active=True
    ).exclude(batch__start_time__isnull=True).exclude(batch__end_time__isnull=True).select_related('batch', 'batch__course', 'student')

    if exclude_enrollment_id:
        try:
            exclude_enrollment_id = int(exclude_enrollment_id)
            enrollments = enrollments.exclude(enrollment_id=exclude_enrollment_id)
        except (ValueError, TypeError):
            pass

    for enr in enrollments:
        b = enr.batch
        student_name = enr.student.display_name if enr.student else "This student"
        c_name = b.course.course_name if b.course else ""
        class_desc = f"'{b.batch_name}' ({c_name})" if c_name else f"'{b.batch_name}'"

        # Check 1: Already assigned to the same batch
        if b.batch_id == target_batch.batch_id:
            msg = f"Student {student_name} is already assigned to batch {class_desc}. Cannot add again."
            return b, msg

        # Check 2: Time overlap with another batch
        if times_overlap(target_batch.start_time, target_batch.end_time, b.start_time, b.end_time):
            if dates_overlap(target_batch.start_date, target_batch.end_date, b.start_date, b.end_date):
                exact_same_slot = (
                    target_batch.start_time == b.start_time and
                    target_batch.end_time == b.end_time and
                    (not target_batch.start_date or not b.start_date or target_batch.start_date == b.start_date) and
                    (not target_batch.end_date or not b.end_date or target_batch.end_date == b.end_date)
                )
                if exact_same_slot or check_days_overlap(target_batch.course, b.course):
                    t_str = f"{b.start_time.strftime('%I:%M %p')} - {b.end_time.strftime('%I:%M %p')}"
                    d_str = ""
                    if b.start_date and b.end_date:
                        d_str = f", {b.start_date.strftime('%d/%m/%Y')} to {b.end_date.strftime('%d/%m/%Y')}"
                    elif b.start_date:
                        d_str = f", from {b.start_date.strftime('%d/%m/%Y')}"
                    msg = f"Student {student_name} is already enrolled in batch '{b.batch_name}' ({c_name}, {t_str}{d_str}). A student cannot be assigned to multiple batches at the same time."
                    return b, msg
    return None, None


def assign_fees_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    try:
        user = User.objects.get(user_id=request.session['user_id'])
    except User.DoesNotExist:
        request.session.flush()
        return redirect('login')
    
    from academics.models import Course, Batch, StudentEnrollment
    from finance.models import StudentFee, FeeType
    from decimal import Decimal
    
    sync_enrollment_fees(user.user_id)
    
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        course_id = request.POST.get('course_id')
        batch_id = request.POST.get('batch_id')
        due_date_str = request.POST.get('due_date')
        remarks = request.POST.get('remarks')
        
        reg_fee = Decimal(request.POST.get('reg_fee') or '0')
        reg_disc = Decimal(request.POST.get('reg_disc') or '0')
        course_fee = Decimal(request.POST.get('course_fee') or '0')
        course_disc = Decimal(request.POST.get('course_disc') or '0')
        mat_fee = Decimal(request.POST.get('mat_fee') or '0')
        mat_disc = Decimal(request.POST.get('mat_disc') or '0')
        
        total_amt = reg_fee + course_fee + mat_fee
        total_disc = reg_disc + course_disc + mat_disc
        final_amt = max(Decimal('0'), total_amt - total_disc)
        
        try:
            student = User.objects.get(user_id=student_id)
            course = Course.objects.filter(course_id=course_id).first() if course_id else None
            batch = Batch.objects.filter(batch_id=batch_id).first() if batch_id else None
            
            if batch:
                existing_enr = StudentEnrollment.objects.filter(student=student, course=course).first() if course else None
                clash_batch, clash_msg = check_student_time_conflict(
                    student_id=student.user_id,
                    target_batch=batch,
                    exclude_enrollment_id=existing_enr.enrollment_id if existing_enr else None
                )
                if clash_batch:
                    messages.error(request, clash_msg)
                    return redirect('assign_fees')

            sf, created = StudentFee.objects.update_or_create(
                student=student,
                course=course,
                defaults={
                    'batch': batch,
                    'total_amount': total_amt,
                    'discount_amount': total_disc,
                    'final_amount': final_amt,
                    'due_date': due_date_str or (batch.end_date if batch else None),
                    'status': 1,
                    'created_by': user.user_id
                }
            )
            if course:
                StudentEnrollment.objects.get_or_create(
                    student=student,
                    course=course,
                    defaults={
                        'batch': batch,
                        'joining_date': batch.start_date if batch else None,
                        'status': 1
                    }
                )
            messages.success(request, f'Fees of ₹{final_amt:,.2f} assigned successfully to {student.display_name or student.first_name}!')
            return redirect('pending_fees')
        except Exception as e:
            messages.error(request, f'Error assigning fees: {str(e)}')
            return redirect('assign_fees')
        
    students = User.objects.filter(role__role_name='Student', is_active=True).order_by('first_name', 'last_name')
    courses = Course.objects.filter(is_active=True).order_by('course_name')
    batches = Batch.objects.filter(is_active=True).order_by('batch_name')
    fee_types = FeeType.objects.filter(is_active=True).order_by('fee_type_name')
    
    return render(request, 'website/assign_fees.html', {
        'user': user,
        'page_title': 'Assign Fees',
        'students': students,
        'courses': courses,
        'batches': batches,
        'fee_types': fee_types,
    })


def pending_fees_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    try:
        user = User.objects.get(user_id=request.session['user_id'])
    except User.DoesNotExist:
        request.session.flush()
        return redirect('login')
    
    from academics.models import Course, Batch
    from finance.models import StudentFee, FeePayment
    from datetime import date
    from django.db.models import Sum
    
    sync_enrollment_fees(user.user_id)
    
    courses = Course.objects.filter(is_active=True).order_by('course_name')
    batches = Batch.objects.filter(is_active=True).order_by('batch_name')
    
    selected_course = request.GET.get('course', '')
    selected_batch = request.GET.get('batch', '')
    status_filter = request.GET.get('status', 'all')
    
    today = date.today()
    pending_qs = StudentFee.objects.select_related('student', 'course', 'batch').filter(status__in=[1, 2])
    
    if selected_course:
        pending_qs = pending_qs.filter(course_id=selected_course)
    if selected_batch:
        pending_qs = pending_qs.filter(batch_id=selected_batch)
        
    pending_list = []
    for idx, sf in enumerate(pending_qs.order_by('due_date'), start=1):
        paid = FeePayment.objects.filter(student_fee=sf).aggregate(total=Sum('paid_amount'))['total'] or 0
        pending_amt = max(0, sf.final_amount - paid)
        if pending_amt <= 0:
            continue
            
        is_overdue = bool(sf.due_date and sf.due_date < today)
        days_overdue = (today - sf.due_date).days if is_overdue else 0
        
        if status_filter == 'pending' and is_overdue:
            continue
        elif status_filter == 'overdue' and not is_overdue:
            continue
            
        stu = sf.student
        stu_name = stu.display_name or f"{stu.first_name} {stu.last_name}".strip() if stu else '-'
        
        pending_list.append({
            'index': idx,
            'student_id': stu.user_id if stu else '',
            'student_fee_id': sf.student_fee_id,
            'student_name': stu_name,
            'course_name': sf.course.course_name if sf.course else '-',
            'batch_name': sf.batch.batch_name if sf.batch else '-',
            'total_fees': f"{sf.final_amount:,.2f}",
            'paid_amount': f"{paid:,.2f}",
            'pending_amount': f"{pending_amt:,.2f}",
            'due_date': sf.due_date.strftime('%d/%m/%Y') if sf.due_date else '-',
            'days_overdue': days_overdue if is_overdue else '-',
            'is_overdue': is_overdue,
        })
        
    return render(request, 'website/pending_fees.html', {
        'user': user,
        'page_title': 'Pending Fees',
        'courses': courses,
        'batches': batches,
        'pending_list': pending_list,
        'selected_course': selected_course,
        'selected_batch': selected_batch,
        'status_filter': status_filter,
    })

def receipts_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    try:
        user = User.objects.get(user_id=request.session['user_id'])
    except User.DoesNotExist:
        request.session.flush()
        return redirect('login')
    
    from finance.models import FeeReceipt, FeePayment
    payment_mode_map = {1: 'Cash', 2: 'UPI', 3: 'Credit Card', 4: 'Debit Card', 5: 'Net Banking'}
    
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')
    receipt_no = request.GET.get('receipt_no', '').strip()
    
    receipts_qs = FeeReceipt.objects.select_related('student', 'fee_payment').order_by('-receipt_date')
    if from_date:
        receipts_qs = receipts_qs.filter(receipt_date__date__gte=from_date)
    if to_date:
        receipts_qs = receipts_qs.filter(receipt_date__date__lte=to_date)
    if receipt_no:
        receipts_qs = receipts_qs.filter(receipt_no__icontains=receipt_no)
        
    receipt_list = []
    for r in receipts_qs:
        stu = r.student
        fp = r.fee_payment
        stu_name = stu.display_name or f"{stu.first_name} {stu.last_name}".strip() if stu else '-'
        receipt_list.append({
            'receipt_id': r.receipt_id,
            'receipt_no': r.receipt_no,
            'date': r.receipt_date.strftime('%d/%m/%Y') if r.receipt_date else '-',
            'student_name': stu_name,
            'amount': f"{r.total_amount:,.2f}",
            'mode': payment_mode_map.get(fp.payment_mode, 'Other') if fp else '-',
            'transaction_no': (fp.transaction_no if fp and fp.transaction_no else '-') or '-',
        })
        
    return render(request, 'website/receipts.html', {
        'user': user,
        'page_title': 'Receipts',
        'receipts': receipt_list,
        'from_date': from_date,
        'to_date': to_date,
        'receipt_no': receipt_no,
    })

def refunds_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    try:
        user = User.objects.get(user_id=request.session['user_id'])
    except User.DoesNotExist:
        request.session.flush()
        return redirect('login')
    
    from finance.models import FeeRefund
    refunds_qs = FeeRefund.objects.select_related('student', 'receipt').order_by('-refund_date')
    
    refund_list = []
    for rf in refunds_qs:
        stu = rf.student
        stu_name = stu.display_name or f"{stu.first_name} {stu.last_name}".strip() if stu else '-'
        refund_list.append({
            'refund_id': rf.refund_id,
            'refund_no': f"RFND{rf.refund_id:04d}",
            'receipt_no': rf.receipt.receipt_no if rf.receipt else '-',
            'student_name': stu_name,
            'amount': f"{rf.refund_amount:,.2f}",
            'date': rf.refund_date.strftime('%d/%m/%Y') if rf.refund_date else '-',
            'reason': rf.reason or '-',
            'status': 'Approved' if rf.approved_by else 'Pending',
        })
        
    return render(request, 'website/refunds.html', {
        'user': user,
        'page_title': 'Refunds',
        'refunds': refund_list,
    })


def reports_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    try:
        user = User.objects.get(user_id=request.session['user_id'])
    except User.DoesNotExist:
        request.session.flush()
        return redirect('login')
    
    from academics.models import Course, Batch
    from finance.models import FeePayment, StudentFee, FeeReceipt
    from datetime import date
    from django.db.models import Sum, Q
    
    sync_enrollment_fees(user.user_id)
    
    students = User.objects.filter(role__role_name='Student', is_active=True).order_by('first_name', 'last_name')
    courses = Course.objects.filter(is_active=True).order_by('course_name')
    batches = Batch.objects.filter(is_active=True).order_by('batch_name')
    
    # 1. Collection Report Tab
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')
    course_id = request.GET.get('course_id', '')
    batch_id = request.GET.get('batch_id', '')
    
    payments_qs = FeePayment.objects.select_related('student_fee', 'student_fee__student', 'student_fee__course', 'student_fee__batch').order_by('-payment_date')
    if from_date:
        payments_qs = payments_qs.filter(payment_date__date__gte=from_date)
    if to_date:
        payments_qs = payments_qs.filter(payment_date__date__lte=to_date)
    if course_id:
        payments_qs = payments_qs.filter(student_fee__course_id=course_id)
    if batch_id:
        payments_qs = payments_qs.filter(student_fee__batch_id=batch_id)
        
    total_collection_val = payments_qs.aggregate(total=Sum('paid_amount'))['total'] or 0
    cash_val = payments_qs.filter(payment_mode=1).aggregate(total=Sum('paid_amount'))['total'] or 0
    upi_val = payments_qs.filter(payment_mode=2).aggregate(total=Sum('paid_amount'))['total'] or 0
    card_val = payments_qs.filter(payment_mode__in=[3, 4]).aggregate(total=Sum('paid_amount'))['total'] or 0
    
    payment_mode_map = {1: 'Cash', 2: 'UPI', 3: 'Card', 4: 'Card', 5: 'Net Banking'}
    collection_items = []
    for p in payments_qs:
        stu = p.student_fee.student if p.student_fee else None
        stu_name = stu.display_name or f"{stu.first_name} {stu.last_name}".strip() if stu else '-'
        collection_items.append({
            'date': p.payment_date.strftime('%d/%m/%Y') if p.payment_date else '-',
            'receipt_no': p.receipt_no or f"RCP-{p.fee_payment_id:04d}",
            'student_name': stu_name,
            'amount': f"{p.paid_amount:,.2f}",
            'mode': payment_mode_map.get(p.payment_mode, 'Other')
        })
        
    # 2. Pending Fees Report Tab
    today = date.today()
    pending_fees_qs = StudentFee.objects.select_related('student', 'course', 'batch').filter(status__in=[1, 2])
    if course_id:
        pending_fees_qs = pending_fees_qs.filter(course_id=course_id)
    if batch_id:
        pending_fees_qs = pending_fees_qs.filter(batch_id=batch_id)
        
    total_pending_val = 0
    total_overdue_val = 0
    due_this_month_val = 0
    due_later_val = 0
    pending_report_items = []
    
    for sf in pending_fees_qs:
        paid = FeePayment.objects.filter(student_fee=sf).aggregate(total=Sum('paid_amount'))['total'] or 0
        pend_amt = max(0, sf.final_amount - paid)
        if pend_amt <= 0:
            continue
            
        total_pending_val += pend_amt
        is_ovd = bool(sf.due_date and sf.due_date < today)
        days_ovd = (today - sf.due_date).days if is_ovd else 0
        if is_ovd:
            total_overdue_val += pend_amt
        elif sf.due_date and sf.due_date.year == today.year and sf.due_date.month == today.month:
            due_this_month_val += pend_amt
        else:
            due_later_val += pend_amt
            
        stu = sf.student
        stu_name = stu.display_name or f"{stu.first_name} {stu.last_name}".strip() if stu else '-'
        pending_report_items.append({
            'student_name': stu_name,
            'course_name': sf.course.course_name if sf.course else '-',
            'batch_name': sf.batch.batch_name if sf.batch else '-',
            'total_fees': f"{sf.final_amount:,.2f}",
            'paid_amount': f"{paid:,.2f}",
            'pending_amount': f"{pend_amt:,.2f}",
            'due_date': sf.due_date.strftime('%d/%m/%Y') if sf.due_date else '-',
            'days_overdue': days_ovd if is_ovd else '-',
        })
        
    # 3. Student Ledger Tab
    ledger_student_id = request.GET.get('student_id', '')
    selected_ledger_student = None
    ledger_total_fees = 0
    ledger_total_paid = 0
    ledger_total_pending = 0
    ledger_items = []
    
    if ledger_student_id:
        try:
            selected_ledger_student = User.objects.get(user_id=ledger_student_id)
        except User.DoesNotExist:
            selected_ledger_student = None
    elif students.exists():
        selected_ledger_student = students.first()
        ledger_student_id = str(selected_ledger_student.user_id)
        
    if selected_ledger_student:
        stu_fees = StudentFee.objects.filter(student=selected_ledger_student)
        ledger_total_fees = stu_fees.aggregate(total=Sum('final_amount'))['total'] or 0
        stu_payments = FeePayment.objects.filter(student_fee__student=selected_ledger_student).order_by('payment_date')
        ledger_total_paid = stu_payments.aggregate(total=Sum('paid_amount'))['total'] or 0
        ledger_total_pending = max(0, ledger_total_fees - ledger_total_paid)
        
        running_balance = 0
        for sf in stu_fees.order_by('created_date'):
            running_balance += sf.final_amount
            ledger_items.append({
                'date': sf.created_date.strftime('%d/%m/%Y') if sf.created_date else '-',
                'particulars': f"Assigned - {sf.course.course_name if sf.course else 'Course Fee'}",
                'receipt_no': '-',
                'debit': f"{sf.final_amount:,.2f}",
                'credit': '-',
                'balance': f"{running_balance:,.2f}"
            })
        for p in stu_payments:
            running_balance -= p.paid_amount
            ledger_items.append({
                'date': p.payment_date.strftime('%d/%m/%Y') if p.payment_date else '-',
                'particulars': 'Payment Received',
                'receipt_no': p.receipt_no or f"RCP-{p.fee_payment_id:04d}",
                'debit': '-',
                'credit': f"{p.paid_amount:,.2f}",
                'balance': f"{running_balance:,.2f}"
            })
            
    return render(request, 'website/reports.html', {
        'user': user,
        'page_title': 'Reports',
        'students': students,
        'courses': courses,
        'batches': batches,
        # Collection Report
        'total_collection': f"{total_collection_val:,.2f}",
        'cash_collection': f"{cash_val:,.2f}",
        'upi_collection': f"{upi_val:,.2f}",
        'card_collection': f"{card_val:,.2f}",
        'collection_items': collection_items,
        'from_date': from_date,
        'to_date': to_date,
        'course_id': course_id,
        'batch_id': batch_id,
        # Pending Report
        'total_pending': f"{total_pending_val:,.2f}",
        'total_overdue': f"{total_overdue_val:,.2f}",
        'due_this_month': f"{due_this_month_val:,.2f}",
        'due_later': f"{due_later_val:,.2f}",
        'pending_report_items': pending_report_items,
        # Ledger
        'ledger_student_id': ledger_student_id,
        'selected_ledger_student': selected_ledger_student,
        'ledger_total_fees': f"{ledger_total_fees:,.2f}",
        'ledger_total_paid': f"{ledger_total_paid:,.2f}",
        'ledger_total_pending': f"{ledger_total_pending:,.2f}",
        'ledger_items': ledger_items,
    })


def courses_batches_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    from users.models import User
    try:

        user = User.objects.get(user_id=request.session['user_id'])

    except User.DoesNotExist:

        request.session.flush()

        return redirect('login')
    
    from academics.models import Course, Batch
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add_course':
            course_code = request.POST.get('course_code')
            if not course_code:
                last_course = Course.objects.exclude(course_code__isnull=True).exclude(course_code='').order_by('-course_id').first()
                if last_course and last_course.course_code.startswith('C'):
                    try:
                        num = int(last_course.course_code[1:]) + 1
                        course_code = f"C{num}"
                    except:
                        course_code = "C1000"
                else:
                    course_code = "C1000"
            
            category = request.POST.get('category')
            if category == 'Custom' and request.POST.get('category_custom'):
                category = request.POST.get('category_custom')
            category = category.strip() if category else None

            days = request.POST.get('days')
            if days == 'Custom' and request.POST.get('days_custom'):
                days = request.POST.get('days_custom')
            days = days.strip() if days else None

            duration_hrs = request.POST.get('duration_hrs')
            if duration_hrs:
                try:
                    from decimal import Decimal
                    duration_hrs = Decimal(str(duration_hrs))
                except:
                    duration_hrs = None
            else:
                duration_hrs = None

            Course.objects.create(
                course_code=course_code,
                course_name=request.POST.get('course_name'),
                category=category,
                duration_months=request.POST.get('duration_months') or None,
                duration_hrs=duration_hrs,
                total_sessions=request.POST.get('total_sessions') or None,
                days=days,
                fee_amount=request.POST.get('fee_amount') or 0.00,
                description=request.POST.get('description'),
                is_active=request.POST.get('status') == 'active',
                created_by=user.user_id
            )
            messages.success(request, 'Course added successfully!')
            return redirect('courses')
        elif action == 'edit_course':
            course_id = request.POST.get('course_id')
            try:
                course = Course.objects.get(course_id=course_id)
                course.course_name = request.POST.get('course_name')
                
                category = request.POST.get('category')
                if category == 'Custom' and request.POST.get('category_custom'):
                    category = request.POST.get('category_custom')
                course.category = category.strip() if category else None

                course.duration_months = request.POST.get('duration_months') or None

                duration_hrs = request.POST.get('duration_hrs')
                if duration_hrs:
                    try:
                        from decimal import Decimal
                        duration_hrs = Decimal(str(duration_hrs))
                    except:
                        duration_hrs = None
                else:
                    duration_hrs = None
                course.duration_hrs = duration_hrs

                course.total_sessions = request.POST.get('total_sessions') or None

                days = request.POST.get('days')
                if days == 'Custom' and request.POST.get('days_custom'):
                    days = request.POST.get('days_custom')
                course.days = days.strip() if days else None

                course.fee_amount = request.POST.get('fee_amount') or 0.00
                course.description = request.POST.get('description') or None
                course.is_active = (request.POST.get('status') == 'active')
                course.save()
                messages.success(request, 'Course updated successfully!')
            except Exception as e:
                messages.error(request, f'Error updating course: {str(e)}')
            return redirect('courses')
        elif action == 'delete_course':
            course_id = request.POST.get('course_id')
            try:
                batch_count = Batch.objects.filter(course_id=course_id).count()
                if batch_count > 0:
                    messages.error(request, f'Cannot delete course because it is assigned to {batch_count} batch(es). Please delete or reassign those batches first.')
                else:
                    Course.objects.filter(course_id=course_id).delete()
                    messages.success(request, 'Course deleted successfully!')
            except Exception as e:
                messages.error(request, f'Error deleting course: {str(e)}')
            return redirect('courses')
        elif action == 'add_batch':
            batch_code = request.POST.get('batch_code')
            if not batch_code:
                last_batch = Batch.objects.exclude(batch_code__isnull=True).exclude(batch_code='').order_by('-batch_id').first()
                if last_batch and last_batch.batch_code.startswith('B'):
                    try:
                        num = int(last_batch.batch_code[1:]) + 1
                        batch_code = f"B{num}"
                    except:
                        batch_code = "B1000"
                else:
                    batch_code = "B1000"
                    
            course_id = request.POST.get('course_id')
            teacher_id = request.POST.get('teacher_id')
            start_date = request.POST.get('start_date') or None
            end_date = request.POST.get('end_date') or None
            start_time = request.POST.get('start_time') or None
            end_time = request.POST.get('end_time') or None
            course = Course.objects.filter(course_id=course_id).first() if course_id else None

            if teacher_id and start_time and end_time:
                clash_b, clash_m = check_teacher_time_conflict(
                    teacher_id=teacher_id,
                    start_time=start_time,
                    end_time=end_time,
                    start_date=start_date,
                    end_date=end_date,
                    course=course
                )
                if clash_b:
                    messages.error(request, clash_m)
                    return redirect('/courses/?tab=batches')

            Batch.objects.create(
                batch_code=batch_code,
                batch_name=request.POST.get('batch_name'),
                course_id=course_id,
                teacher_id=teacher_id if teacher_id else None,
                start_date=start_date,
                end_date=end_date,
                start_time=start_time,
                end_time=end_time,
                capacity=request.POST.get('capacity') or None,
                is_active=request.POST.get('status') == 'active',
                created_by=user.user_id
            )
            if course_id and teacher_id:
                from academics.models import UserCourse
                UserCourse.objects.get_or_create(user_id=teacher_id, course_id=course_id, defaults={'is_active': True})
            sync_batch_timetable(user.user_id)
            messages.success(request, 'Batch added successfully!')
            return redirect('/courses/?tab=batches')
        elif action == 'edit_batch':
            batch_id = request.POST.get('batch_id')
            try:
                batch = Batch.objects.get(batch_id=batch_id)
                course_id = request.POST.get('course_id') or batch.course_id
                course = Course.objects.filter(course_id=course_id).first() if course_id else batch.course
                teacher_id = request.POST.get('teacher_id')
                start_date = request.POST.get('start_date') or None
                end_date = request.POST.get('end_date') or None
                start_time = request.POST.get('start_time') or None
                end_time = request.POST.get('end_time') or None

                if teacher_id and start_time and end_time:
                    clash_b, clash_m = check_teacher_time_conflict(
                        teacher_id=teacher_id,
                        start_time=start_time,
                        end_time=end_time,
                        start_date=start_date,
                        end_date=end_date,
                        course=course,
                        exclude_batch_id=batch.batch_id
                    )
                    if clash_b:
                        messages.error(request, clash_m)
                        return redirect('/courses/?tab=batches')

                batch.batch_name = request.POST.get('batch_name')
                if course_id:
                    batch.course_id = course_id
                batch.teacher_id = teacher_id if teacher_id else None
                batch.start_date = start_date
                batch.end_date = end_date
                batch.start_time = start_time
                batch.end_time = end_time
                batch.capacity = request.POST.get('capacity') or None
                batch.is_active = (request.POST.get('status') == 'active')
                batch.save()
                if batch.course_id and batch.teacher_id:
                    from academics.models import UserCourse
                    UserCourse.objects.get_or_create(user_id=batch.teacher_id, course_id=batch.course_id, defaults={'is_active': True})
                sync_batch_timetable(user.user_id)
                messages.success(request, 'Batch updated successfully!')
            except Exception as e:
                messages.error(request, f'Error updating batch: {str(e)}')
            return redirect('/courses/?tab=batches')
        elif action == 'delete_batch':
            batch_id = request.POST.get('batch_id')
            try:
                from academics.models import StudentEnrollment, Timetable
                enroll_count = StudentEnrollment.objects.filter(batch_id=batch_id).count()
                if enroll_count > 0:
                    messages.error(request, f'Cannot delete batch because it has {enroll_count} student enrollment(s).')
                else:
                    Timetable.objects.filter(batch_id=batch_id).delete()
                    Batch.objects.filter(batch_id=batch_id).delete()
                    messages.success(request, 'Batch deleted successfully!')
            except Exception as e:
                messages.error(request, f'Error deleting batch: {str(e)}')
            return redirect('/courses/?tab=batches')
        return redirect('courses')
        
    courses = Course.objects.all().order_by('-course_id')
    batches = Batch.objects.select_related('course', 'teacher').all().order_by('-batch_id')
    teachers = User.objects.filter(role__role_name='Teacher', is_active=True).order_by('first_name', 'last_name')
    
    from academics.models import UserCourse
    import json
    
    teachers_list = []
    for t in teachers:
        uc_cids = list(UserCourse.objects.filter(user=t, is_active=True).values_list('course_id', flat=True))
        b_cids = list(Batch.objects.filter(teacher=t).values_list('course_id', flat=True))
        all_cids = sorted(list(set(uc_cids + b_cids)))
        teachers_list.append({
            'user_id': t.user_id,
            'name': t.display_name or f"{t.first_name} {t.last_name}".strip(),
            'code': t.user_code or '',
            'course_ids': all_cids
        })
    teachers_json = json.dumps(teachers_list)

    courses_list = []
    for c in courses:
        courses_list.append({
            'course_id': c.course_id,
            'course_code': c.course_code or '',
            'course_name': c.course_name,
            'category': c.category or '',
            'duration_months': c.duration_months or 0,
            'duration_hrs': float(c.duration_hrs) if c.duration_hrs is not None else 0.0,
            'total_sessions': c.total_sessions or 0,
            'days': c.days or '',
            'fee_amount': float(c.fee_amount) if c.fee_amount is not None else 0.0,
            'is_active': c.is_active,
            'description': c.description or '',
        })
    courses_json = json.dumps(courses_list)
    
    return render(request, 'website/courses_batches.html', {
        'user': user,
        'page_title': 'Courses & Batches',
        'courses': courses,
        'courses_json': courses_json,
        'batches': batches,
        'teachers': teachers,
        'teachers_json': teachers_json,
    })

def admin_dashboard_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
        
    try:

        
        user = User.objects.get(user_id=request.session['user_id'])

        
    except User.DoesNotExist:

        
        request.session.flush()

        
        return redirect('login')
    from users.models import Role, RoleGroup, RoleAccess, MasterMenu
    
    roles = Role.objects.all().select_related('role_group')
    users = User.objects.all().select_related('role')
    # Fetch menus and construct a full tree hierarchy (Parents, children, and subchildren)
    raw_menus = list(MasterMenu.objects.filter(is_active=True).order_by('display_order', 'menu_id'))
    def get_ordered_menus(parent_id=None, level=0):
        result = []
        for m in raw_menus:
            if m.parent_menu_id == parent_id:
                m.level = level
                result.append(m)
                result.extend(get_ordered_menus(m.menu_id, level + 1))
        return result
    menus = get_ordered_menus(None)
    
    # RBAC Enforcement
    try:
        admin_menu = MasterMenu.objects.get(menu_name='Admin')
        admin_access = RoleAccess.objects.get(role=user.role, menu=admin_menu)
    except (MasterMenu.DoesNotExist, RoleAccess.DoesNotExist):
        admin_access = None

    if not admin_access or not admin_access.view_access:
        messages.error(request, 'You do not have permission to view the Admin Dashboard.')
        return redirect('index')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        # RBAC Check for POST actions
        if action == 'save_settings':
            import json, os
            from django.conf import settings
            
            phone_length = request.POST.get('phone_length', 10)
            email_length = request.POST.get('email_length', 255)
            password_expire = request.POST.get('password_expire', 90)
            attendance_from_date = request.POST.get('attendance_from_date', '').strip()
            attendance_to_date = request.POST.get('attendance_to_date', '').strip()
            
            data = {
                'phone_length': int(phone_length) if phone_length else 10,
                'email_length': int(email_length) if email_length else 255,
                'password_expire': int(password_expire) if password_expire else 90,
                'attendance_from_date': attendance_from_date,
                'attendance_to_date': attendance_to_date,
            }
            path = os.path.join(settings.BASE_DIR, 'security_settings.json')
            with open(path, 'w') as fh:
                json.dump(data, fh, indent=4)
            
            messages.success(request, 'Settings saved successfully.')
            return redirect('/admin-dashboard/?tab=settings')
            
        if action == 'create_user' and not admin_access.add_access:
            messages.error(request, 'You do not have permission to add records.')
            return redirect('/admin-dashboard/')
            
        if action == 'save_permissions' and not admin_access.edit_access:
            messages.error(request, 'You do not have permission to edit records.')
            return redirect('/admin-dashboard/')
            
        if action == 'save_menu_orders':
            if not admin_access.edit_access:
                messages.error(request, 'You do not have permission to edit records.')
                return redirect('/admin-dashboard/?tab=menu')
            
            for key, value in request.POST.items():
                if key.startswith('order_'):
                    menu_id = key.replace('order_', '')
                    try:
                        menu = MasterMenu.objects.get(menu_id=menu_id)
                        menu.display_order = int(value)
                        menu.save()
                    except Exception as e:
                        pass
            
            messages.success(request, 'Menu order updated successfully!')
            return redirect('/admin-dashboard/?tab=menu')

        if action == 'save_menu':
            if request.POST.get('menu_id') and not admin_access.edit_access:
                messages.error(request, 'You do not have permission to edit records.')
                return redirect('/admin-dashboard/?tab=menu')
            elif not request.POST.get('menu_id') and not admin_access.add_access:
                messages.error(request, 'You do not have permission to add records.')
                return redirect('/admin-dashboard/?tab=menu')
                
        if action == 'delete_menu' and not admin_access.delete_access:
            messages.error(request, 'You do not have permission to delete records.')
            return redirect('/admin-dashboard/?tab=menu')

        if action == 'create_user':
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            email = request.POST.get('email', '')
            phone = request.POST.get('phone', '')
            password = request.POST.get('password', '')
            role_id = request.POST.get('role_id')
            
            confirm_password = request.POST.get('confirm_password', '')
            if password and password != confirm_password:
                messages.error(request, "Password and confirm password must match.")
                return redirect('/admin-dashboard/?tab=users')
            
            try:
                role = Role.objects.get(role_id=role_id)
                
                # Auto-generate user_code for Students and Teachers
                user_code = None
                if role.role_name.lower() == 'student':
                    last_student = User.objects.filter(role=role, user_code__startswith='S').order_by('-user_id').first()
                    if last_student and last_student.user_code:
                        try:
                            last_num = int(last_student.user_code[1:])
                            user_code = f"S{last_num + 1}"
                        except:
                            user_code = "S1000"
                    else:
                        user_code = "S1000"
                elif role.role_name.lower() == 'teacher':
                    last_teacher = User.objects.filter(role=role, user_code__startswith='T').order_by('-user_id').first()
                    if last_teacher and last_teacher.user_code:
                        try:
                            last_num = int(last_teacher.user_code[1:])
                            user_code = f"T{last_num + 1}"
                        except:
                            user_code = "T2000"
                    else:
                        user_code = "T2000"
                        
                User.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    display_name=f"{first_name} {last_name}".strip(),
                    email=email,
                    phone=phone,
                    password=password,
                    role=role,
                    user_code=user_code
                )
                messages.success(request, f'User {first_name} {last_name} created successfully!')
            except Exception as e:
                messages.error(request, 'Failed to create user.')
                print(e)
            return redirect('/admin-dashboard/?tab=users')
            
        elif action == 'save_permissions':
            role_id = request.POST.get('role_id')
            role = Role.objects.get(role_id=role_id)
            try:
                # Optimized Bulk Operation to eliminate N+1 network latency
                role_access_instances = []
                for menu in menus:
                    m_id = str(menu.menu_id)
                    view = request.POST.get(f'view_{m_id}') == 'on'
                    add = request.POST.get(f'add_{m_id}') == 'on'
                    edit = request.POST.get(f'edit_{m_id}') == 'on'
                    delete = request.POST.get(f'delete_{m_id}') == 'on'
                    export = request.POST.get(f'export_{m_id}') == 'on'
                    
                    role_access_instances.append(
                        RoleAccess(
                            role=role, 
                            menu=menu,
                            view_access=view,
                            add_access=add,
                            edit_access=edit,
                            delete_access=delete,
                            export_access=export,
                            approve_access=False,
                            created_by=user.user_id
                        )
                    )
                
                # Optimized Bulk Operation to eliminate N+1 network latency
                # Delete existing permissions for this role (1 query)
                RoleAccess.objects.filter(role=role).delete()
                # Bulk insert all new permissions (1 query)
                RoleAccess.objects.bulk_create(role_access_instances)
                messages.success(request, f'Role permissions for {role.role_name} updated successfully!')
            except Exception as e:
                messages.error(request, 'Failed to update role permissions.')
                print(e)
            return redirect(f'/admin-dashboard/?tab=roles&role_id={role_id}')

    
        elif action == 'save_menu':
            menu_id = request.POST.get('menu_id')
            menu_name = request.POST.get('menu_name')
            url_page = request.POST.get('url_page')
            is_active = request.POST.get('is_active') == 'on'
            
            try:
                if menu_id:
                    menu = MasterMenu.objects.get(menu_id=menu_id)
                    menu.menu_name = menu_name
                    menu.url_page = url_page
                    menu.is_active = is_active
                    menu.display_order = display_order
                    menu.save()
                    messages.success(request, f'Menu {menu_name} updated successfully!')
                else:
                    MasterMenu.objects.create(
                        menu_name=menu_name,
                        url_page=url_page,
                        is_active=is_active,
                        display_order=display_order
                    )
                    messages.success(request, f'Menu {menu_name} created successfully!')
            except Exception as e:
                messages.error(request, 'Failed to save menu.')
                print(e)
            return redirect('/admin-dashboard/?tab=menu')
            
        elif action == 'delete_menu':
            menu_id = request.POST.get('menu_id')
            try:
                menu = MasterMenu.objects.get(menu_id=menu_id)
                menu_name = menu.menu_name
                menu.delete()
                messages.success(request, f'Menu {menu_name} deleted successfully!')
            except Exception as e:
                messages.error(request, 'Failed to delete menu.')
            return redirect('/admin-dashboard/?tab=menu')

    tab = request.GET.get('tab', 'dashboard')
    
    # Selected role for permissions matrix
    selected_role_id = request.GET.get('role_id')
    selected_role = None
    role_access_map = {}
    if roles.exists():
        if not selected_role_id:
            selected_role_id = roles.first().role_id
        
        try:
            selected_role = Role.objects.get(role_id=selected_role_id)
            access_records = RoleAccess.objects.filter(role=selected_role)
            for access in access_records:
                role_access_map[access.menu_id] = access
        except Role.DoesNotExist:
            selected_role = roles.first()
    
    from users.models import UserLoginDetails
    from django.db.models import Q
    from datetime import datetime
    
    audit_user = request.GET.get('audit_user', '')
    audit_status = request.GET.get('audit_status', '')
    audit_from = request.GET.get('audit_from', '')
    audit_to = request.GET.get('audit_to', '')
    
    audit_qs = UserLoginDetails.objects.select_related('user').order_by('-login_date')
    
    if audit_user:
        audit_qs = audit_qs.filter(user_id=audit_user)
        
    if audit_status:
        audit_qs = audit_qs.filter(remarks__icontains=audit_status)
        
    if audit_from:
        try:
            from_dt = datetime.strptime(audit_from, '%Y-%m-%d').date()
            audit_qs = audit_qs.filter(login_date__date__gte=from_dt)
        except: pass
        
    if audit_to:
        try:
            to_dt = datetime.strptime(audit_to, '%Y-%m-%d').date()
            audit_qs = audit_qs.filter(login_date__date__lte=to_dt)
        except: pass

    audit_logs = audit_qs[:100]
    
    context = {
        'page_title': 'Admin',
        'active_tab': tab,
        'user': user,
        'roles': roles,
        'users': users,
        'menus': menus,
        'audit_logs': audit_logs,
        'selected_role': selected_role,
        'role_access_map': role_access_map,
    }
    return render(request, 'website/admin_dashboard.html', context)

def student_course_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
        
    try:

        
        user = User.objects.get(user_id=request.session['user_id'])

        
    except User.DoesNotExist:

        
        request.session.flush()

        
        return redirect('login')
    from academics.models import Course, StudentEnrollment, Batch
    from django.db.models import Q
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'edit_student_allocation':
            enrollment_id = request.POST.get('enrollment_id')
            student_id = request.POST.get('student_id')
            batch_id = request.POST.get('batch_id')
            try:
                enrollment = StudentEnrollment.objects.get(enrollment_id=enrollment_id)
                target_student = User.objects.get(user_id=student_id) if student_id else enrollment.student
                target_batch = Batch.objects.get(batch_id=batch_id) if batch_id else enrollment.batch

                if target_batch:
                    clash_b, clash_m = check_student_time_conflict(
                        student_id=target_student.user_id,
                        target_batch=target_batch,
                        exclude_enrollment_id=enrollment.enrollment_id
                    )
                    if clash_b:
                        messages.error(request, clash_m)
                        return redirect('student_course')

                enrollment.student = target_student
                if target_batch:
                    enrollment.batch = target_batch
                    enrollment.course = target_batch.course
                enrollment.save()
                
                # Sync fee
                if enrollment.course and enrollment.student:
                    from finance.models import StudentFee
                    fee_amt = enrollment.course.fee_amount or 0
                    sf, sf_created = StudentFee.objects.get_or_create(
                        student=enrollment.student,
                        course=enrollment.course,
                        defaults={
                            'batch': enrollment.batch,
                            'total_amount': fee_amt,
                            'discount_amount': 0,
                            'final_amount': fee_amt,
                            'due_date': (enrollment.batch.end_date if enrollment.batch else None) or (enrollment.batch.start_date if enrollment.batch else None),
                            'status': 1,
                            'created_by': user.user_id
                        }
                    )
                    if not sf_created:
                        sf.batch = enrollment.batch
                        if (sf.total_amount == 0 or sf.final_amount == 0) and fee_amt > 0:
                            sf.total_amount = fee_amt
                            sf.final_amount = fee_amt - (sf.discount_amount or 0)
                        if not sf.due_date and enrollment.batch and enrollment.batch.end_date:
                            sf.due_date = enrollment.batch.end_date
                        sf.save()
                messages.success(request, 'Student allocation updated successfully.')
            except Exception as e:
                messages.error(request, f'Error updating student allocation: {str(e)}')
            return redirect('student_course')
        elif action == 'delete_student_allocation':
            enrollment_id = request.POST.get('enrollment_id')
            try:
                enrollment = StudentEnrollment.objects.filter(enrollment_id=enrollment_id).first()
                if enrollment:
                    from finance.models import StudentFee, FeePayment
                    sf = StudentFee.objects.filter(student=enrollment.student, course=enrollment.course).first()
                    if sf and not FeePayment.objects.filter(student_fee=sf).exists():
                        sf.delete()
                    enrollment.delete()
                messages.success(request, 'Student allocation deleted successfully.')
            except Exception as e:
                messages.error(request, f'Error deleting student allocation: {str(e)}')
            return redirect('student_course')

    enrollments = StudentEnrollment.objects.select_related('student', 'course', 'batch', 'batch__teacher').exclude(batch__isnull=True).order_by('-created_date')
    courses = Course.objects.filter(is_active=True)
    batches = Batch.objects.select_related('course', 'teacher').filter(is_active=True).order_by('batch_name')
    students = User.objects.filter(role__role_name='Student', is_active=True).order_by('display_name')
    
    # Filter logic
    search = request.GET.get('search', '')
    course_id = request.GET.get('course_id', '')
    
    if search:
        enrollments = enrollments.filter(
            Q(student__display_name__icontains=search) | 
            Q(student__user_code__icontains=search) | 
            Q(course__course_name__icontains=search)
        )
        
    if course_id:
        enrollments = enrollments.filter(course_id=course_id)
        
    
    # Role based filtering
    if user.role and user.role.role_name == 'Student':
        enrollments = enrollments.filter(student=user)
        
    return render(request, 'website/student_course.html', {
        'user': user,
        'page_title': 'Allocation Details',
        'allocations': enrollments,
        'courses': courses,
        'batches': batches,
        'students': students,
    })

def student_allocation_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
        
    try:
        user = User.objects.get(user_id=request.session['user_id'])
    except User.DoesNotExist:
        request.session.flush()
        return redirect('login')
    from academics.models import Course, StudentEnrollment, Batch
    from django.db.models import Q
    from django.http import JsonResponse
    import json
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'allocate_student':
            student_id = request.POST.get('student_id')
            batch_id = request.POST.get('batch_id')
            
            try:
                student = User.objects.get(user_id=student_id)
                batch = Batch.objects.get(batch_id=batch_id)

                # Check if already enrolled in this exact batch
                if StudentEnrollment.objects.filter(student=student, batch=batch, status=1).exists():
                    c_name = batch.course.course_name if batch.course else ""
                    class_desc = f"'{batch.batch_name}' ({c_name})" if c_name else f"'{batch.batch_name}'"
                    messages.error(request, f"Student {student.display_name} is already assigned to batch {class_desc}. Cannot add again.")
                    return redirect('student_allocation')

                # Check if already enrolled in this course with an active batch
                existing_course_batch = StudentEnrollment.objects.filter(student=student, course=batch.course, status=1, batch__isnull=False).first()
                if existing_course_batch:
                    c_name = batch.course.course_name if batch.course else "this course"
                    messages.error(request, f"Student {student.display_name} is already assigned to batch '{existing_course_batch.batch.batch_name}' for course '{c_name}'. Cannot add again.")
                    return redirect('student_allocation')

                clash_b, clash_m = check_student_time_conflict(
                    student_id=student.user_id,
                    target_batch=batch
                )
                if clash_b:
                    messages.error(request, clash_m)
                    return redirect('student_allocation')

                # If student had an enrollment for this course without a batch assigned
                existing_unassigned = StudentEnrollment.objects.filter(student=student, course=batch.course, batch__isnull=True).first()
                if existing_unassigned:
                    existing_unassigned.batch = batch
                    existing_unassigned.save()
                    messages.success(request, 'Student allocated successfully.')
                else:
                    StudentEnrollment.objects.create(
                        student=student,
                        course=batch.course,
                        batch=batch,
                        joining_date=batch.start_date,
                        status=1
                    )
                    messages.success(request, 'Student allocated successfully.')
                
                # Sync fee
                from finance.models import StudentFee
                fee_amt = batch.course.fee_amount or 0
                sf, sf_created = StudentFee.objects.get_or_create(
                    student=student,
                    course=batch.course,
                    defaults={
                        'batch': batch,
                        'total_amount': fee_amt,
                        'discount_amount': 0,
                        'final_amount': fee_amt,
                        'due_date': batch.end_date or batch.start_date,
                        'status': 1,
                        'created_by': user.user_id
                    }
                )
                if not sf_created:
                    sf.batch = batch
                    if (sf.total_amount == 0 or sf.final_amount == 0) and fee_amt > 0:
                        sf.total_amount = fee_amt
                        sf.final_amount = fee_amt - (sf.discount_amount or 0)
                    if not sf.due_date and batch.end_date:
                        sf.due_date = batch.end_date
                    sf.save()
            except Exception as e:
                messages.error(request, f'Error allocating student: {str(e)}')
            return redirect('student_allocation')
        elif action == 'edit_student_allocation':
            enrollment_id = request.POST.get('enrollment_id')
            student_id = request.POST.get('student_id')
            batch_id = request.POST.get('batch_id')
            try:
                enrollment = StudentEnrollment.objects.get(enrollment_id=enrollment_id)
                target_student = User.objects.get(user_id=student_id) if student_id else enrollment.student
                target_batch = Batch.objects.get(batch_id=batch_id) if batch_id else enrollment.batch

                if target_batch:
                    clash_b, clash_m = check_student_time_conflict(
                        student_id=target_student.user_id,
                        target_batch=target_batch,
                        exclude_enrollment_id=enrollment.enrollment_id
                    )
                    if clash_b:
                        messages.error(request, clash_m)
                        return redirect('student_allocation')

                enrollment.student = target_student
                if target_batch:
                    enrollment.batch = target_batch
                    enrollment.course = target_batch.course
                enrollment.save()
                
                # Sync fee
                if enrollment.course and enrollment.student:
                    from finance.models import StudentFee
                    fee_amt = enrollment.course.fee_amount or 0
                    sf, sf_created = StudentFee.objects.get_or_create(
                        student=enrollment.student,
                        course=enrollment.course,
                        defaults={
                            'batch': enrollment.batch,
                            'total_amount': fee_amt,
                            'discount_amount': 0,
                            'final_amount': fee_amt,
                            'due_date': (enrollment.batch.end_date if enrollment.batch else None) or (enrollment.batch.start_date if enrollment.batch else None),
                            'status': 1,
                            'created_by': user.user_id
                        }
                    )
                    if not sf_created:
                        sf.batch = enrollment.batch
                        if (sf.total_amount == 0 or sf.final_amount == 0) and fee_amt > 0:
                            sf.total_amount = fee_amt
                            sf.final_amount = fee_amt - (sf.discount_amount or 0)
                        if not sf.due_date and enrollment.batch and enrollment.batch.end_date:
                            sf.due_date = enrollment.batch.end_date
                        sf.save()
                messages.success(request, 'Student allocation updated successfully.')
            except Exception as e:
                messages.error(request, f'Error updating student allocation: {str(e)}')
            return redirect('student_allocation')
        elif action == 'delete_student_allocation':
            enrollment_id = request.POST.get('enrollment_id')
            try:
                enrollment = StudentEnrollment.objects.filter(enrollment_id=enrollment_id).first()
                if enrollment:
                    from finance.models import StudentFee, FeePayment
                    sf = StudentFee.objects.filter(student=enrollment.student, course=enrollment.course).first()
                    if sf and not FeePayment.objects.filter(student_fee=sf).exists():
                        sf.delete()
                    enrollment.delete()
                messages.success(request, 'Student allocation deleted successfully.')
            except Exception as e:
                messages.error(request, f'Error deleting student allocation: {str(e)}')
            return redirect('student_allocation')
            
    # GET Request
    allocations = StudentEnrollment.objects.select_related('student', 'course', 'batch', 'batch__teacher').exclude(batch__isnull=True).order_by('-created_date')

    # Filter logic
    search = request.GET.get('search', '').strip()
    course_filter = request.GET.get('course_id', '').strip()
    batch_filter = request.GET.get('batch_id', '').strip()
    teacher_filter = request.GET.get('teacher_id', '').strip()

    if search:
        allocations = allocations.filter(
            Q(student__display_name__icontains=search) |
            Q(student__user_code__icontains=search) |
            Q(student__phone__icontains=search) |
            Q(course__course_name__icontains=search) |
            Q(batch__batch_name__icontains=search) |
            Q(batch__batch_code__icontains=search) |
            Q(batch__teacher__display_name__icontains=search)
        )
    if course_filter:
        allocations = allocations.filter(course_id=course_filter)
    if batch_filter:
        allocations = allocations.filter(batch_id=batch_filter)
    if teacher_filter:
        allocations = allocations.filter(batch__teacher_id=teacher_filter)

    courses = Course.objects.filter(is_active=True).order_by('course_name')
    # Pre-fetch for the modal dropdowns
    students = User.objects.filter(role__role_name='Student', is_active=True).order_by('display_name')
    teachers = User.objects.filter(role__role_name='Teacher', is_active=True).order_by('display_name')
    batches = Batch.objects.select_related('course', 'teacher').filter(is_active=True).order_by('batch_name')
    
    # Calculate remaining capacity for batches
    for batch in batches:
        enrolled_count = StudentEnrollment.objects.filter(batch=batch, status=1).count()
        batch.remaining_capacity = (batch.capacity or 0) - enrolled_count
    
    return render(request, 'website/student_allocation.html', {
        'user': user,
        'page_title': 'Student Course Allocation',
        'allocations': allocations,
        'students': students,
        'teachers': teachers,
        'batches': batches,
        'courses': courses,
    })

from django.http import JsonResponse
def api_get_student_details(request):
    user_id = request.GET.get('id')
    try:
        student = User.objects.get(user_id=user_id)
        return JsonResponse({
            'success': True,
            'student_code': student.user_code,
            'name': student.display_name,
            'phone': student.phone
        })
    except:
        return JsonResponse({'success': False})

def api_get_student_fee_details(request):
    user_id = request.GET.get('id') or request.GET.get('student_id')
    course_id = request.GET.get('course_id')
    try:
        from users.models import User
        from academics.models import StudentEnrollment, Course, Batch
        from finance.models import StudentFee, FeePayment
        from django.db.models import Sum

        if not user_id:
            return JsonResponse({'success': False, 'error': 'Student ID is required'})

        student = User.objects.get(user_id=user_id)
        sync_enrollment_fees(request.session.get('user_id'))

        sf_qs = StudentFee.objects.filter(student=student)
        if course_id:
            sf_qs = sf_qs.filter(course_id=course_id)
        sf = sf_qs.order_by('-student_fee_id').first()

        if sf:
            paid = FeePayment.objects.filter(student_fee=sf).aggregate(total=Sum('paid_amount'))['total'] or 0
            pending = max(0, float(sf.final_amount) - float(paid))
            return JsonResponse({
                'success': True,
                'student_id': student.user_id,
                'student_name': student.display_name or f"{student.first_name} {student.last_name}".strip(),
                'student_fee_id': sf.student_fee_id,
                'course_id': sf.course.course_id if sf.course else '',
                'course_name': sf.course.course_name if sf.course else '',
                'batch_id': sf.batch.batch_id if sf.batch else '',
                'batch_name': sf.batch.batch_name if sf.batch else '',
                'course_fee': float(sf.total_amount),
                'reg_fee': 0.0,
                'total_amount': float(sf.total_amount),
                'discount_amount': float(sf.discount_amount or 0),
                'paid_amount': float(paid),
                'payable_amount': float(pending)
            })
        else:
            enrollment = StudentEnrollment.objects.filter(student=student).order_by('-enrollment_id').first()
            if enrollment and enrollment.course:
                fee_amt = float(enrollment.course.fee_amount or 0)
                return JsonResponse({
                    'success': True,
                    'student_id': student.user_id,
                    'student_name': student.display_name or f"{student.first_name} {student.last_name}".strip(),
                    'student_fee_id': '',
                    'course_id': enrollment.course.course_id,
                    'course_name': enrollment.course.course_name,
                    'batch_id': enrollment.batch.batch_id if enrollment.batch else '',
                    'batch_name': enrollment.batch.batch_name if enrollment.batch else '',
                    'course_fee': fee_amt,
                    'reg_fee': 0.0,
                    'total_amount': fee_amt,
                    'discount_amount': 0.0,
                    'paid_amount': 0.0,
                    'payable_amount': fee_amt
                })
            return JsonResponse({
                'success': True,
                'student_id': student.user_id,
                'student_name': student.display_name or f"{student.first_name} {student.last_name}".strip(),
                'student_fee_id': '',
                'course_id': '',
                'course_name': '',
                'batch_id': '',
                'batch_name': '',
                'course_fee': 0.0,
                'reg_fee': 0.0,
                'total_amount': 0.0,
                'discount_amount': 0.0,
                'paid_amount': 0.0,
                'payable_amount': 0.0
            })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

from django.http import JsonResponse
def api_get_batch_details(request):
    batch_id = request.GET.get('id')
    try:
        from academics.models import Batch, StudentEnrollment
        batch = Batch.objects.get(batch_id=batch_id)
        enrolled_count = StudentEnrollment.objects.filter(batch=batch, status=1).count()
        remaining = (batch.capacity or 0) - enrolled_count
        
        return JsonResponse({
            'success': True,
            'course_id': batch.course.course_id,
            'course_name': batch.course.course_name,
            'batch_code': batch.batch_code,
            'batch_name': batch.batch_name,
            'teacher_id': batch.teacher.user_id if batch.teacher else '',
            'teacher_name': batch.teacher.display_name if batch.teacher else '',
            'teacher_phone': batch.teacher.phone if batch.teacher else '',
            'start_time': batch.start_time.strftime('%H:%M') if batch.start_time else '',
            'end_time': batch.end_time.strftime('%H:%M') if batch.end_time else '',
            'remaining_capacity': remaining
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def teacher_allocation_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
        
    try:

        
        user = User.objects.get(user_id=request.session['user_id'])

        
    except User.DoesNotExist:

        
        request.session.flush()

        
        return redirect('login')
    from academics.models import Course, Batch
    from django.db.models import Q
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'allocate_teacher':
            teacher_id = request.POST.get('teacher_id')
            batch_id = request.POST.get('batch_id')
            
            try:
                teacher = User.objects.get(user_id=teacher_id)
                batch = Batch.objects.get(batch_id=batch_id)

                if batch.teacher_id and str(batch.teacher_id) == str(teacher.user_id):
                    messages.error(request, f"Teacher {teacher.display_name} is already assigned to batch '{batch.batch_name}'. Cannot add again.")
                    return redirect('teacher_allocation')

                if batch.teacher_id and str(batch.teacher_id) != str(teacher.user_id):
                    curr_t_name = batch.teacher.display_name if batch.teacher else "another teacher"
                    messages.error(request, f"Batch '{batch.batch_name}' is already assigned to teacher {curr_t_name}. To reassign, please edit the existing allocation.")
                    return redirect('teacher_allocation')

                clash_b, clash_m = check_teacher_time_conflict(
                    teacher_id=teacher.user_id,
                    start_time=batch.start_time,
                    end_time=batch.end_time,
                    start_date=batch.start_date,
                    end_date=batch.end_date,
                    course=batch.course,
                    exclude_batch_id=batch.batch_id
                )
                if clash_b:
                    messages.error(request, clash_m)
                    return redirect('teacher_allocation')

                batch.teacher = teacher
                batch.save()
                if batch.course_id:
                    from academics.models import UserCourse
                    UserCourse.objects.get_or_create(user_id=teacher.user_id, course_id=batch.course_id, defaults={'is_active': True})
                sync_batch_timetable(user.user_id)
                messages.success(request, 'Teacher allocated successfully.')
            except Exception as e:
                messages.error(request, f'Error allocating teacher: {str(e)}')
            return redirect('teacher_allocation')
        elif action == 'edit_teacher_allocation':
            batch_id = request.POST.get('batch_id')
            teacher_id = request.POST.get('teacher_id')
            try:
                batch = Batch.objects.get(batch_id=batch_id)
                teacher = User.objects.get(user_id=teacher_id)

                clash_b, clash_m = check_teacher_time_conflict(
                    teacher_id=teacher.user_id,
                    start_time=batch.start_time,
                    end_time=batch.end_time,
                    start_date=batch.start_date,
                    end_date=batch.end_date,
                    course=batch.course,
                    exclude_batch_id=batch.batch_id
                )
                if clash_b:
                    messages.error(request, clash_m)
                    return redirect('teacher_allocation')

                batch.teacher = teacher
                batch.save()
                if batch.course_id:
                    from academics.models import UserCourse
                    UserCourse.objects.get_or_create(user_id=teacher.user_id, course_id=batch.course_id, defaults={'is_active': True})
                sync_batch_timetable(user.user_id)
                messages.success(request, 'Teacher allocation updated successfully.')
            except Exception as e:
                messages.error(request, f'Error updating teacher allocation: {str(e)}')
            return redirect('teacher_allocation')
        elif action == 'delete_teacher_allocation':
            batch_id = request.POST.get('batch_id')
            try:
                batch = Batch.objects.get(batch_id=batch_id)
                batch.teacher = None
                batch.save()
                sync_batch_timetable(user.user_id)
                messages.success(request, 'Teacher allocation removed successfully.')
            except Exception as e:
                messages.error(request, f'Error removing teacher allocation: {str(e)}')
            return redirect('teacher_allocation')
            
    # GET Request
    allocations = Batch.objects.select_related('course', 'teacher').exclude(teacher__isnull=True).order_by('-created_date')
    
    # Filter logic
    search = request.GET.get('search', '')
    if search:
        allocations = allocations.filter(
            Q(teacher__display_name__icontains=search) | 
            Q(teacher__user_code__icontains=search) | 
            Q(course__course_name__icontains=search) |
            Q(batch_name__icontains=search)
        )
        
    # Pre-fetch for the modal dropdowns
    teachers = User.objects.filter(role__role_name='Teacher', is_active=True).order_by('display_name')
    batches = Batch.objects.select_related('course').filter(is_active=True).order_by('batch_name')
    
    return render(request, 'website/teacher_allocation.html', {
        'user': user,
        'page_title': 'Teacher Class Allocation',
        'allocations': allocations,
        'teachers': teachers,
        'batches': batches,
    })

from django.http import JsonResponse
def api_get_teacher_details(request):
    user_id = request.GET.get('id')
    try:
        from users.models import User
        teacher = User.objects.get(user_id=user_id)
        return JsonResponse({
            'success': True,
            'teacher_code': teacher.user_code,
            'name': teacher.display_name,
            'phone': teacher.phone
        })
    except:
        return JsonResponse({'success': False})

def api_check_conflict(request):
    check_type = request.GET.get('type')  # 'teacher' or 'student'
    
    if check_type == 'teacher':
        teacher_id = request.GET.get('teacher_id')
        batch_id = request.GET.get('batch_id')
        start_time = request.GET.get('start_time')
        end_time = request.GET.get('end_time')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        course_id = request.GET.get('course_id')
        exclude_batch_id = request.GET.get('exclude_batch_id')
        
        from academics.models import Batch, Course
        course = Course.objects.filter(course_id=course_id).first() if course_id else None
        
        if batch_id:
            target_batch = Batch.objects.filter(batch_id=batch_id).select_related('course', 'teacher').first()
            if target_batch:
                start_time = target_batch.start_time
                end_time = target_batch.end_time
                start_date = target_batch.start_date
                end_date = target_batch.end_date
                course = target_batch.course

                # Check if this batch is already assigned to a teacher (in Add mode)
                is_edit_same = bool(exclude_batch_id and str(exclude_batch_id) == str(target_batch.batch_id))
                if not is_edit_same and teacher_id and target_batch.teacher_id:
                    if str(target_batch.teacher_id) == str(teacher_id):
                        teacher_name = target_batch.teacher.display_name if target_batch.teacher else "This teacher"
                        return JsonResponse({
                            'has_conflict': True,
                            'conflict_message': f"Teacher {teacher_name} is already assigned to batch '{target_batch.batch_name}'. Cannot add again."
                        })
                    else:
                        curr_t_name = target_batch.teacher.display_name if target_batch.teacher else "another teacher"
                        return JsonResponse({
                            'has_conflict': True,
                            'conflict_message': f"Batch '{target_batch.batch_name}' is already assigned to teacher {curr_t_name}. To reassign, please edit the existing allocation."
                        })

                if not exclude_batch_id:
                    exclude_batch_id = target_batch.batch_id

        clash_batch, msg = check_teacher_time_conflict(
            teacher_id=teacher_id,
            start_time=start_time,
            end_time=end_time,
            start_date=start_date,
            end_date=end_date,
            course=course,
            exclude_batch_id=exclude_batch_id
        )
        return JsonResponse({
            'has_conflict': bool(clash_batch),
            'conflict_message': msg or ''
        })

    elif check_type == 'student':
        student_id = request.GET.get('student_id')
        batch_id = request.GET.get('batch_id')
        exclude_enrollment_id = request.GET.get('exclude_enrollment_id')

        from academics.models import Batch, StudentEnrollment
        from users.models import User

        if student_id and batch_id:
            target_batch = Batch.objects.filter(batch_id=batch_id).select_related('course').first()
            student_obj = User.objects.filter(user_id=student_id).first()
            student_name = student_obj.display_name if student_obj else "This student"

            # Check 1: Already assigned to the SAME batch
            same_batch_enr = StudentEnrollment.objects.filter(
                student_id=student_id,
                batch_id=batch_id,
                status=1
            )
            if exclude_enrollment_id:
                try:
                    same_batch_enr = same_batch_enr.exclude(enrollment_id=int(exclude_enrollment_id))
                except (ValueError, TypeError):
                    pass

            if same_batch_enr.exists():
                batch_name = target_batch.batch_name if target_batch else "this batch"
                c_name = target_batch.course.course_name if target_batch and target_batch.course else ""
                class_desc = f"'{batch_name}' ({c_name})" if c_name else f"'{batch_name}'"
                return JsonResponse({
                    'has_conflict': True,
                    'conflict_message': f"Student {student_name} is already assigned to batch {class_desc}. Cannot add again."
                })

            # Check 2: Already enrolled in the same course with an active batch (in Add mode)
            if not exclude_enrollment_id and target_batch:
                existing_course_enr = StudentEnrollment.objects.filter(
                    student_id=student_id,
                    course=target_batch.course,
                    status=1,
                    batch__isnull=False
                ).first()
                if existing_course_enr:
                    c_name = target_batch.course.course_name if target_batch.course else "this course"
                    return JsonResponse({
                        'has_conflict': True,
                        'conflict_message': f"Student {student_name} is already assigned to batch '{existing_course_enr.batch.batch_name}' for course '{c_name}'. Cannot add again."
                    })

        clash_batch, msg = check_student_time_conflict(
            student_id=student_id,
            target_batch=batch_id,
            exclude_enrollment_id=exclude_enrollment_id
        )
        return JsonResponse({
            'has_conflict': bool(clash_batch),
            'conflict_message': msg or ''
        })

    return JsonResponse({'has_conflict': False, 'conflict_message': ''})

def attendance_log_view(request):
    if 'user_id' not in request.session:
        return redirect('login')

    from users.models import User
    try:
        try:

            user = User.objects.get(user_id=request.session['user_id'])

        except User.DoesNotExist:

            request.session.flush()

            return redirect('login')
    except User.DoesNotExist:
        return redirect('login')
        
    from academics.models import LeaveRequest
    
    if request.method == 'POST':
        action = request.POST.get('action')
        request_id = request.POST.get('leave_request_id')
        if action == 'Revoke' and request_id:
            lr = LeaveRequest.objects.get(leave_request_id=request_id)
            lr.manager_approval_status = 'Pending'
            lr.manager_approval_on = None
            lr.save()

            if lr.user_type == 'Student':
                from academics.models import StudentAttendanceDetail
                StudentAttendanceDetail.objects.filter(
                    student=lr.user,
                    student_attendance__attendance_date__gte=lr.from_date,
                    student_attendance__attendance_date__lte=lr.to_date
                ).update(approval_status='Pending')
            elif lr.user_type == 'Teacher':
                from academics.models import TeacherAttendanceDetail
                TeacherAttendanceDetail.objects.filter(
                    teacher=lr.user,
                    teacher_attendance__attendance_date__gte=lr.from_date,
                    teacher_attendance__attendance_date__lte=lr.to_date
                ).update(approval_status='Pending')

            messages.success(request, 'Request revoked and moved back to approvals!')
        return redirect(f'/attendance-log/?tab={request.POST.get("tab", request.GET.get("tab", "students"))}')
        
    tab = request.GET.get('tab', 'students')
    
    # Filter
    filter_status = request.GET.get('filter_status', '')
    filter_from = request.GET.get('filter_from', '')
    filter_to = request.GET.get('filter_to', '')
    
    from academics.models import LeaveRequest
    
    leave_qs = LeaveRequest.objects.select_related('user').exclude(manager_approval_status='Pending')
    
    if tab == 'students':
        leave_qs = leave_qs.filter(user_type='Student')
    else:
        leave_qs = leave_qs.filter(user_type='Teacher')
        
    if filter_status:
        leave_qs = leave_qs.filter(manager_approval_status=filter_status)
    if filter_from:
        try:
            leave_qs = leave_qs.filter(from_date__gte=filter_from)
        except: pass
    if filter_to:
        try:
            leave_qs = leave_qs.filter(to_date__lte=filter_to)
        except: pass
        
    leaves = leave_qs.order_by('-applied_date')

    context = {
        'page_title': 'Attendance Log',
        'user': user,
        'tab': tab,
        'leaves': leaves,
    }
    return render(request, 'website/attendance_log.html', context)

def attendance_approval_view(request):
    if 'user_id' not in request.session:
        return redirect('login')

    from users.models import User
    try:
        try:

            user = User.objects.get(user_id=request.session['user_id'])

        except User.DoesNotExist:

            request.session.flush()

            return redirect('login')
    except User.DoesNotExist:
        return redirect('login')
        
    from academics.models import LeaveRequest
    
    if request.method == 'POST':
        action = request.POST.get('action')
        request_id = request.POST.get('leave_request_id')
        if action in ['Approve', 'Reject'] and request_id:
            from django.utils import timezone
            lr = LeaveRequest.objects.get(leave_request_id=request_id)
            new_status = 'Approved' if action == 'Approve' else 'Rejected'
            lr.manager_approval_status = new_status
            lr.manager_approval_on = timezone.now()
            lr.save()

            if lr.user_type == 'Student':
                from academics.models import StudentAttendanceDetail
                StudentAttendanceDetail.objects.filter(
                    student=lr.user,
                    student_attendance__attendance_date__gte=lr.from_date,
                    student_attendance__attendance_date__lte=lr.to_date
                ).update(approval_status=new_status)
            elif lr.user_type == 'Teacher':
                from academics.models import TeacherAttendanceDetail
                TeacherAttendanceDetail.objects.filter(
                    teacher=lr.user,
                    teacher_attendance__attendance_date__gte=lr.from_date,
                    teacher_attendance__attendance_date__lte=lr.to_date
                ).update(approval_status=new_status)

            messages.success(request, f'Request {action}d successfully!')
        return redirect(f'/attendance-approval/?tab={request.POST.get("tab", request.GET.get("tab", "students"))}')
        
    tab = request.GET.get('tab', 'students')
    filter_status = request.GET.get('filter_status', 'Pending') # Default to pending for approvals
    filter_from = request.GET.get('filter_from', '')
    filter_to = request.GET.get('filter_to', '')
    
    leave_qs = LeaveRequest.objects.select_related('user').all()
    
    if tab == 'students':
        leave_qs = leave_qs.filter(user_type='Student')
    else:
        leave_qs = leave_qs.filter(user_type='Teacher')
        
    if filter_status:
        leave_qs = leave_qs.filter(manager_approval_status=filter_status)
    if filter_from:
        try:
            leave_qs = leave_qs.filter(from_date__gte=filter_from)
        except: pass
    if filter_to:
        try:
            leave_qs = leave_qs.filter(to_date__lte=filter_to)
        except: pass
        
    leaves = leave_qs.order_by('-applied_date')

    context = {
        'page_title': 'Attendance Approval',
        'user': user,
        'tab': tab,
        'leaves': leaves,
    }
    return render(request, 'website/attendance_approval.html', context)

def audit_logs_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
        
    from users.models import User, UserLoginDetails
    from django.db.models import Q
    from datetime import datetime
    
    users = User.objects.all()
    
    audit_user = request.GET.get('audit_user', '')
    audit_status = request.GET.get('audit_status', '')
    audit_from = request.GET.get('audit_from', '')
    audit_to = request.GET.get('audit_to', '')
    
    audit_qs = UserLoginDetails.objects.select_related('user').order_by('-login_date')
    
    if audit_user:
        audit_qs = audit_qs.filter(user_id=audit_user)
        
    if audit_status:
        audit_qs = audit_qs.filter(remarks__icontains=audit_status)
        
    if audit_from:
        try:
            from_dt = datetime.strptime(audit_from, '%Y-%m-%d').date()
            audit_qs = audit_qs.filter(login_date__date__gte=from_dt)
        except: pass
        
    if audit_to:
        try:
            to_dt = datetime.strptime(audit_to, '%Y-%m-%d').date()
            audit_qs = audit_qs.filter(login_date__date__lte=to_dt)
        except: pass

    audit_logs = audit_qs[:100]
    
    return render(request, 'website/audit_logs.html', {
        'page_title': 'Audit Logs',
        'users': users,
        'audit_logs': audit_logs
    })

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def mobile_login_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            uname = data.get('username')
            upass = data.get('password')
            
            user = User.objects.select_related('role').get(first_name=uname, password=upass)
            if user.is_active:
                return JsonResponse({
                    'success': True, 
                    'user_id': user.user_id,
                    'first_name': user.first_name,
                    'role': user.role.role_name if user.role else 'Student'
                })
            else:
                return JsonResponse({'success': False, 'error': 'Account disabled'})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Invalid credentials'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def mobile_students_api(request):
    if request.method == 'GET':
        students = User.objects.filter(role__role_name__iexact='student').values(
            'user_id', 'first_name', 'email', 'phone'
        )
        return JsonResponse({'success': True, 'data': list(students)})
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def mobile_teachers_api(request):
    if request.method == 'GET':
        teachers = User.objects.filter(role__role_name__iexact='teacher').values(
            'user_id', 'first_name', 'email', 'phone'
        )
        return JsonResponse({'success': True, 'data': list(teachers)})
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

from academics.models import Course, Timetable

@csrf_exempt
def mobile_courses_api(request):
    if request.method == 'GET':
        courses = Course.objects.filter(is_active=True).values(
            'course_id', 'course_name', 'description'
        )
        return JsonResponse({'success': True, 'data': list(courses)})
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def mobile_timetable_api(request):
    if request.method == 'GET':
        timetables = Timetable.objects.filter(is_active=True).select_related('batch', 'batch__course', 'teacher')
        day = request.GET.get('day')
        batch_id = request.GET.get('batch_id')
        teacher_id = request.GET.get('teacher_id')
        search = request.GET.get('search')
        if day:
            timetables = timetables.filter(day_of_week__iexact=day)
        if batch_id:
            timetables = timetables.filter(batch_id=batch_id)
        if teacher_id:
            timetables = timetables.filter(teacher_id=teacher_id)
        if search:
            timetables = timetables.filter(
                Q(batch__batch_name__icontains=search) |
                Q(batch__course__course_name__icontains=search) |
                Q(teacher__display_name__icontains=search) |
                Q(room_number__icontains=search)
            )
        data = timetables.values(
            'timetable_id', 
            'day_of_week', 
            'start_time', 
            'end_time', 
            'batch__course__course_name',
            'batch__batch_name',
            'teacher__first_name',
            'teacher__display_name',
            'room_number'
        )
        return JsonResponse({'success': True, 'data': list(data)})
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

from users.models import MasterMenu, RoleAccess

@csrf_exempt
def mobile_menus_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            user = User.objects.select_related('role').get(user_id=user_id)
            
            # Get all active menus
            all_menus = list(MasterMenu.objects.filter(is_active=True).order_by('display_order', 'menu_id'))
            
            # Get role access
            if user.role and user.role.role_name.lower() == 'superadmin':
                access_set = {m.menu_id for m in all_menus}
            else:
                access_records = RoleAccess.objects.filter(role=user.role, view_access=True).values_list('menu_id', flat=True)
                access_set = set(access_records)
            
            # We will flatten the menu structure for the mobile grid, or return a list of accessible menus.
            # For simplicity in mobile, let's just return all accessible menus that are NOT parent containers 
            # (i.e. they actually have a url_page), OR we just return all accessible menus.
            mobile_menus = []
            for m in all_menus:
                if m.menu_id in access_set and m.url_page and m.url_page != '#':
                    mobile_menus.append({
                        'menu_id': m.menu_id,
                        'menu_name': m.menu_name,
                        'url_page': m.url_page,
                        'parent_menu_id': m.parent_menu_id
                    })
                    
            return JsonResponse({'success': True, 'data': mobile_menus})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

from finance.models import StudentFee
from academics.models import StudentAttendance, StudentAttendanceDetail

@csrf_exempt
def mobile_attendance_api(request):
    if request.method == 'GET':
        records = StudentAttendanceDetail.objects.all().select_related(
            'student', 'student_attendance', 'student_attendance__course'
        ).values(
            'student_attendance__attendance_date',
            'student__first_name',
            'student__display_name',
            'student_attendance__course__course_name',
            'attendance_status',
            'remarks'
        )[:50]
        status_map = {1: 'Present', 2: 'Absent', 3: 'Late', 4: 'Leave'}
        formatted = []
        for r in records:
            formatted.append({
                'date': str(r['student_attendance__attendance_date']) if r['student_attendance__attendance_date'] else '',
                'student__first_name': r['student__display_name'] or r['student__first_name'] or '',
                'course__course_name': r['student_attendance__course__course_name'] or 'General',
                'status': status_map.get(r['attendance_status'], 'Present'),
                'remarks': r['remarks'] or ''
            })
        return JsonResponse({'success': True, 'data': formatted})
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def mobile_fees_api(request):
    if request.method == 'GET':
        records = StudentFee.objects.all().select_related('student').values(
            'student__first_name', 'total_fee_amount', 'fee_status', 'due_date'
        )[:50]
        return JsonResponse({'success': True, 'data': list(records)})
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def mobile_users_api(request):
    if request.method == 'GET':
        records = User.objects.all().select_related('role').values(
            'first_name', 'email', 'role__role_name', 'is_active'
        )[:50]
        return JsonResponse({'success': True, 'data': list(records)})
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def mobile_roles_api(request):
    if request.method == 'GET':
        from users.models import Role
        records = Role.objects.all().values('role_name', 'is_active')
        return JsonResponse({'success': True, 'data': list(records)})
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def mobile_auditlogs_api(request):
    if request.method == 'GET':
        from users.models import AuditLog
        records = AuditLog.objects.all().select_related('user').values(
            'user__first_name', 'action', 'table_name', 'action_date'
        ).order_by('-action_date')[:50]
        return JsonResponse({'success': True, 'data': list(records)})
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def mobile_events_api(request):
    if request.method == 'GET':
        return JsonResponse({'success': True, 'data': [{'event_name': 'Annual Day', 'date': '2026-12-01'}]})
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def mobile_settings_api(request):
    if request.method == 'GET':
        return JsonResponse({'success': True, 'data': [{'setting': 'Theme', 'value': 'Light'}, {'setting': 'Version', 'value': '1.0'}]})
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def mobile_generic_api(request):
    if request.method == 'GET':
        menu_name = request.GET.get('menu', '').lower()
        data = []
        
        try:
            if 'allocation' in menu_name or 'enrollment' in menu_name:
                from academics.models import StudentEnrollment
                records = StudentEnrollment.objects.all().select_related('student', 'course', 'batch').values(
                    'student__first_name', 'course__course_name', 'batch__batch_name', 'joining_date'
                )[:50]
                data = list(records)
            elif 'receipt' in menu_name or 'refund' in menu_name:
                from finance.models import FeeReceipt
                records = FeeReceipt.objects.all().select_related('fee_payment__student_fee__student').values(
                    'receipt_no', 'student__first_name', 'receipt_date'
                )[:50]
                data = list(records)
            elif 'notification' in menu_name:
                data = [{'Title': 'Welcome!', 'Message': 'Welcome to Melos Music Mobile App.'}]
            elif 'venue' in menu_name:
                data = [{'Venue': 'Main Hall', 'Capacity': '500'}, {'Venue': 'Studio A', 'Capacity': '20'}]
            elif 'admin' in menu_name or 'dashboard' in menu_name:
                data = [{'Module': menu_name.title(), 'Status': 'Active', 'Metrics': 'Available on Web Dashboard'}]
            elif 'menu' in menu_name:
                from users.models import MasterMenu
                records = MasterMenu.objects.all().values('menu_name', 'url_page', 'is_active')[:50]
                data = list(records)
            else:
                data = [{'Module': menu_name.title(), 'Status': 'Available', 'Details': 'Data sync in progress...'}]
                
            return JsonResponse({'success': True, 'data': data})
        except Exception as e:
            return JsonResponse({'success': True, 'data': [{'Error': str(e)}]})
            
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

from django.db.models import Sum, F

@csrf_exempt
def mobile_dashboard_metrics_api(request):
    try:
        from users.models import User
        from academics.models import Course
        from finance.models import StudentFeeInstallment
        from django.db.models import Sum, F
        
        total_students = User.objects.filter(role__role_name__iexact='student').count()
        active_teachers = User.objects.filter(role__role_name__iexact='teacher').count()
        total_courses = Course.objects.filter(is_active=True).count()
        
        pending_fees = StudentFeeInstallment.objects.filter(amount__gt=F('paid_amount')).aggregate(
            total_pending=Sum(F('amount') - F('paid_amount'))
        )['total_pending'] or 0
        
        metrics = [
            {'title': 'Total Students', 'value': str(total_students), 'icon': 'people', 'color': 'blue'},
            {'title': 'Active Teachers', 'value': str(active_teachers), 'icon': 'school', 'color': 'orange'},
            {'title': 'Active Courses', 'value': str(total_courses), 'icon': 'music_note', 'color': 'purple'},
            {'title': 'Pending Fees', 'value': f'${pending_fees}', 'icon': 'money', 'color': 'red'},
        ]
        return JsonResponse({'success': True, 'data': metrics})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Method not allowed'})
