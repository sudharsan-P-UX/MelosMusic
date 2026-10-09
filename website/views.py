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
            
            data = {
                'phone_length': int(phone_length),
                'email_length': int(email_length),
                'password_expire': int(password_expire)
            }
            path = os.path.join(settings.BASE_DIR, 'security_settings.json')
            with open(path, 'w') as fh:
                json.dump(data, fh)
            
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


def timetable_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    try:

    
        user = User.objects.get(user_id=request.session['user_id'])

    
    except User.DoesNotExist:

    
        request.session.flush()

    
        return redirect('login')
    from academics.models import Timetable, Batch
    
    if request.method == 'POST':
        batch_id = request.POST.get('batch_id')
        teacher_id = request.POST.get('teacher_id')
        day_of_week = request.POST.get('day_of_week')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        room_number = request.POST.get('room_number')
        
        batch = Batch.objects.get(batch_id=batch_id)
        teacher = User.objects.get(user_id=teacher_id)
        
        Timetable.objects.create(
            batch=batch,
            teacher=teacher,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            room_number=room_number
        )
        messages.success(request, 'Timetable slot added successfully!')
        return redirect('page', page_name='timetable')
        
    slots = Timetable.objects.all().order_by('start_time')
    batches = Batch.objects.filter(is_active=True)
    teachers = User.objects.filter(role__role_name='Teacher', is_active=True)
    
    # Organize slots by day
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    schedule = {day: [] for day in days}
    for slot in slots:
        if slot.day_of_week in schedule:
            schedule[slot.day_of_week].append(slot)
            
    schedule_data = [(day, schedule[day]) for day in days]
            
    return render(request, 'website/timetable.html', {
        'user': user,
        'schedule_data': schedule_data,
        'days': days,
        'batches': batches,
        'teachers': teachers,
        'page_title': 'Class Schedule'
    })


def student_attendance_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    from users.models import User
    try:

        user = User.objects.get(user_id=request.session['user_id'])

    except User.DoesNotExist:

        request.session.flush()

        return redirect('login')
    from academics.models import Batch, LeaveRequest
    
    if request.method == 'POST':
        if request.POST.get('action') == 'apply_leave':
            student_id = request.POST.get('student_id')
            student = User.objects.get(user_id=student_id)
            LeaveRequest.objects.create(
                user=student,
                user_type='Student',
                from_date=request.POST.get('from_date'),
                to_date=request.POST.get('to_date'),
                no_of_days=request.POST.get('no_of_days') or 1,
                request_type=request.POST.get('request_type'),
                batch_id=request.POST.get('batch_id'),
                created_by=user.user_id
            )
            messages.success(request, 'Attendance request submitted successfully!')
            return redirect('student_attendance')
            
    # Filters
    from academics.models import StudentEnrollment
    allocated_batches = [e.batch for e in StudentEnrollment.objects.filter(student=user, status=1, batch__isnull=False).select_related('batch')]
    
    selected_batch = request.GET.get('batch_id', '')
    selected_student = request.GET.get('student_id', '')
    selected_date = request.GET.get('date', '')
    
    batches = Batch.objects.filter(is_active=True)
    students = User.objects.filter(role__role_name__iexact='student', is_active=True)
    
    details = LeaveRequest.objects.filter(user_type='Student').select_related('user').order_by('-applied_date')
    
    if selected_student:
        details = details.filter(user_id=selected_student)
        
    if selected_date:
        details = details.filter(from_date__lte=selected_date, to_date__gte=selected_date)

    return render(request, 'website/student_attendance.html', {
        'user': user,
        'page_title': 'Student Attendance',
        'batches': batches,
        'students': students,
        'details': details,
        'selected_batch': selected_batch,
        'selected_student': selected_student,
        'selected_date': selected_date
,
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
    from academics.models import LeaveRequest
    
    if request.method == 'POST':
        if request.POST.get('action') == 'apply_leave':
            teacher_id = request.POST.get('teacher_id')
            teacher = User.objects.get(user_id=teacher_id)
            LeaveRequest.objects.create(
                user=teacher,
                user_type='Teacher',
                from_date=request.POST.get('from_date'),
                to_date=request.POST.get('to_date'),
                no_of_days=request.POST.get('no_of_days') or 1,
                request_type=request.POST.get('request_type'),
                batch_id=request.POST.get('batch_id'),
                created_by=user.user_id
            )
            messages.success(request, 'Attendance request submitted successfully!')
            return redirect('teacher_attendance')
            
    # Filters
    from academics.models import Batch
    allocated_batches = list(Batch.objects.filter(teacher=user, is_active=True))
    
    selected_teacher = request.GET.get('teacher_id', '')
    selected_date = request.GET.get('date', '')
    
    teachers = User.objects.filter(role__role_name__iexact='teacher', is_active=True)
    
    details = LeaveRequest.objects.filter(user_type='Teacher').select_related('user').order_by('-applied_date')
    
    if selected_teacher:
        details = details.filter(user_id=selected_teacher)
        
    if selected_date:
        details = details.filter(from_date__lte=selected_date, to_date__gte=selected_date)

    return render(request, 'website/teacher_attendance.html', {
        'user': user,
        'page_title': 'Teacher Attendance',
        'teachers': teachers,
        'details': details,
        'selected_teacher': selected_teacher,
        'selected_date': selected_date
,
        'allocated_batches': allocated_batches
    })


def fee_dashboard_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    try:

        user = User.objects.get(user_id=request.session['user_id'])

    except User.DoesNotExist:

        request.session.flush()

        return redirect('login')
    
    # We will just pass mock data for the dashboard for now since we just created the DB
    return render(request, 'website/fee_dashboard.html', {
        'user': user,
        'page_title': 'Fee Dashboard',
        'todays_collection': '15,000',
        'monthly_collection': '1,25,000',
        'pending_fees': '45,000',
        'overdue_fees': '12,000',
        'students_paid': '80',
        'students_pending': '20'
    })


def fee_collection_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    try:

        user = User.objects.get(user_id=request.session['user_id'])

    except User.DoesNotExist:

        request.session.flush()

        return redirect('login')
    
    from academics.models import Course, Batch
    
    students = User.objects.filter(role__role_name='Student', is_active=True)
    courses = Course.objects.filter(is_active=True)
    batches = Batch.objects.filter(is_active=True)
    
    if request.method == 'POST':
        # Here we would handle the actual payment collection mapping to FeePayment, FeeReceipt, etc.
        messages.success(request, 'Fee payment collected successfully! Receipt generated.')
        return redirect('fee_collection')
        
    return render(request, 'website/fee_collection.html', {
        'user': user,
        'page_title': 'Fee Collection',
        'students': students,
        'courses': courses,
        'batches': batches
    })


def assign_fees_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    try:

        user = User.objects.get(user_id=request.session['user_id'])

    except User.DoesNotExist:

        request.session.flush()

        return redirect('login')
    
    from academics.models import Course, Batch
    from finance.models import StudentFee
    
    students = User.objects.filter(role__role_name='Student', is_active=True)
    courses = Course.objects.filter(is_active=True)
    batches = Batch.objects.filter(is_active=True)
    
    if request.method == 'POST':
        # Here we would map the form data to the StudentFee model
        messages.success(request, 'Fees assigned successfully!')
        return redirect('assign_fees')
        
    return render(request, 'website/assign_fees.html', {
        'user': user,
        'page_title': 'Assign Fees',
        'students': students,
        'courses': courses,
        'batches': batches
    })


def pending_fees_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    try:

        user = User.objects.get(user_id=request.session['user_id'])

    except User.DoesNotExist:

        request.session.flush()

        return redirect('login')
    
    return render(request, 'website/pending_fees.html', {
        'user': user,
        'page_title': 'Pending Fees'
    })

def receipts_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    try:

        user = User.objects.get(user_id=request.session['user_id'])

    except User.DoesNotExist:

        request.session.flush()

        return redirect('login')
    
    return render(request, 'website/receipts.html', {
        'user': user,
        'page_title': 'Receipts'
    })

def refunds_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    try:

        user = User.objects.get(user_id=request.session['user_id'])

    except User.DoesNotExist:

        request.session.flush()

        return redirect('login')
    
    return render(request, 'website/refunds.html', {
        'user': user,
        'page_title': 'Refunds'
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
    
    students = User.objects.filter(role__role_name='Student', is_active=True)
    courses = Course.objects.filter(is_active=True)
    batches = Batch.objects.filter(is_active=True)
    
    return render(request, 'website/reports.html', {
        'user': user,
        'page_title': 'Reports',
        'students': students,
        'courses': courses,
        'batches': batches
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
            
            Course.objects.create(
                course_code=course_code,
                course_name=request.POST.get('course_name'),
                category=request.POST.get('category'),
                duration_months=request.POST.get('duration_months'),
                total_sessions=request.POST.get('total_sessions'),
                days=request.POST.get('days'),
                fee_amount=request.POST.get('fee_amount'),
                description=request.POST.get('description'),
                is_active=request.POST.get('status') == 'active',
                created_by=user.user_id
            )
            messages.success(request, 'Course added successfully!')
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
            Batch.objects.create(
                batch_code=batch_code,
                batch_name=request.POST.get('batch_name'),
                course_id=course_id,
                teacher_id=teacher_id if teacher_id else None,
                start_date=request.POST.get('start_date'),
                end_date=request.POST.get('end_date'),
                start_time=request.POST.get('start_time'),
                end_time=request.POST.get('end_time'),
                capacity=request.POST.get('capacity'),
                is_active=request.POST.get('status') == 'active',
                created_by=user.user_id
            )
            messages.success(request, 'Batch added successfully!')
            return redirect('/courses/?tab=batches')
        return redirect('courses')
        
    courses = Course.objects.all().order_by('-course_id')
    batches = Batch.objects.all().order_by('-batch_id')
    teachers = User.objects.filter(role__role_name='Teacher', is_active=True)
    
    return render(request, 'website/courses_batches.html', {
        'user': user,
        'page_title': 'Courses & Batches',
        'courses': courses,
        'batches': batches,
        'teachers': teachers
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
    # Fetch menus and construct a tree (Parents first, then their children)
    raw_menus = list(MasterMenu.objects.filter(is_active=True).order_by('display_order', 'menu_id'))
    menus = []
    for m in raw_menus:
        if not m.parent_menu_id:
            menus.append(m)
            # Find children for this parent
            for child in raw_menus:
                if child.parent_menu_id == m.menu_id:
                    menus.append(child)
    
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
            
            data = {
                'phone_length': int(phone_length),
                'email_length': int(email_length),
                'password_expire': int(password_expire)
            }
            path = os.path.join(settings.BASE_DIR, 'security_settings.json')
            with open(path, 'w') as fh:
                json.dump(data, fh)
            
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
    from academics.models import Course, StudentEnrollment
    from django.db.models import Q
    
    enrollments = StudentEnrollment.objects.select_related('student', 'course', 'batch', 'batch__teacher').exclude(batch__isnull=True).order_by('-created_date')
    courses = Course.objects.filter(is_active=True)
    
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
        'allocations': enrollments,  # Changed to allocations to match template
        'courses': courses
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
                
                # Check if already enrolled in this course
                existing = StudentEnrollment.objects.filter(student=student, course=batch.course).first()
                if existing:
                    existing.batch = batch
                    existing.save()
                    messages.success(request, 'Student allocation updated successfully.')
                else:
                    StudentEnrollment.objects.create(
                        student=student,
                        course=batch.course,
                        batch=batch,
                        joining_date=batch.start_date,
                        status=1
                    )
                    messages.success(request, 'Student allocated successfully.')
            except Exception as e:
                messages.error(request, f'Error allocating student: {str(e)}')
            return redirect('student_allocation')
            
    # GET Request
    allocations = StudentEnrollment.objects.select_related('student', 'course', 'batch', 'batch__teacher').exclude(batch__isnull=True).order_by('-created_date')
    
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
                
                batch.teacher = teacher
                batch.save()
                messages.success(request, 'Teacher allocated successfully.')
            except Exception as e:
                messages.error(request, f'Error allocating teacher: {str(e)}')
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
            lr.manager_approval_status = 'Approved' if action == 'Approve' else 'Rejected'
            lr.manager_approval_on = timezone.now()
            lr.save()
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
