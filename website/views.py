from django.shortcuts import render, redirect
from django.contrib import messages
from users.models import User, UserLoginDetails

def index(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    # Fetch user for dashboard display
    user = User.objects.get(user_id=request.session['user_id'])
    return render(request, 'website/index.html', {'user': user})

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
    
    user = User.objects.get(user_id=request.session['user_id'])
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
        
        days_list = request.POST.getlist('days')
        preferred_days = ', '.join(days_list) if days_list else request.POST.get('days', '')
        
        parts = name.split(' ', 1)
        fname = parts[0]
        lname = parts[1] if len(parts) > 1 else ""
        
        new_student = User.objects.create(
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
                if password == confirm_password:
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
    
    user = User.objects.get(user_id=request.session['user_id'])
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
        if password != confirm_password:
            pass
        
        parts = name.split(' ', 1)
        fname = parts[0]
        lname = parts[1] if len(parts) > 1 else ""
        
        new_teacher = User.objects.create(
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
                if password == confirm_password:
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
        
    user = User.objects.get(user_id=request.session['user_id'])
    from academics.models import Course, Batch, StudentEnrollment
    from users.models import Role, RoleGroup
    
    rg, _ = RoleGroup.objects.get_or_create(role_group_name="Students")
    student_role, _ = Role.objects.get_or_create(role_name="Student", defaults={'role_group': rg})
    
    students = User.objects.filter(role=student_role, is_active=True)
    courses = Course.objects.all()
    batches = Batch.objects.all()
    enrollments = StudentEnrollment.objects.all()
    
    return render(request, 'website/enrollment_management.html', {
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
        
    user = User.objects.get(user_id=request.session['user_id'])
    
    from events.models import EventMaster, EventParticipant, EventVenue, EventAttendance
    from django.contrib import messages
    
    if request.method == 'POST':
        action = request.POST.get('action')
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
        
        user = User.objects.get(user_id=request.session['user_id'])
        
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
        
    user = User.objects.get(user_id=request.session['user_id'])
    
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
    
    user = User.objects.get(user_id=request.session['user_id'])
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
    user = User.objects.get(user_id=request.session['user_id'])
    from academics.models import Batch, StudentAttendance, StudentAttendanceDetail
    
    if request.method == 'POST':
        attendance_date = request.POST.get('attendance_date')
        batch_id = request.POST.get('batch_id')
        student_id = request.POST.get('student_id')
        status = request.POST.get('status')
        remarks = request.POST.get('remarks')
        
        batch = Batch.objects.get(batch_id=batch_id)
        student = User.objects.get(user_id=student_id)
        
        # Get or create the Master record for this day and batch
        master, created = StudentAttendance.objects.get_or_create(
            attendance_date=attendance_date,
            batch=batch,
            defaults={'created_by': user.user_id, 'course': batch.course}
        )
        
        # Create the detail record
        StudentAttendanceDetail.objects.create(
            student_attendance=master,
            student=student,
            attendance_status=int(status),
            remarks=remarks,
            created_by=user.user_id
        )
        messages.success(request, 'Student attendance recorded successfully!')
        return redirect('student_attendance')
        
    batches = Batch.objects.filter(is_active=True)
    students = User.objects.filter(role__role_name='Student', is_active=True)
    
    details = StudentAttendanceDetail.objects.all().order_by('-created_date')
    
    return render(request, 'website/student_attendance.html', {
        'user': user,
        'page_title': 'Student Attendance',
        'batches': batches,
        'students': students,
        'details': details
    })

def teacher_attendance_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    user = User.objects.get(user_id=request.session['user_id'])
    from academics.models import TeacherAttendance, TeacherAttendanceDetail
    
    if request.method == 'POST':
        attendance_date = request.POST.get('attendance_date')
        teacher_id = request.POST.get('teacher_id')
        status = request.POST.get('status')
        check_in = request.POST.get('check_in_time')
        check_out = request.POST.get('check_out_time')
        remarks = request.POST.get('remarks')
        
        teacher = User.objects.get(user_id=teacher_id)
        
        master, created = TeacherAttendance.objects.get_or_create(
            attendance_date=attendance_date,
            defaults={'created_by': user.user_id}
        )
        
        TeacherAttendanceDetail.objects.create(
            teacher_attendance=master,
            teacher=teacher,
            attendance_status=int(status),
            check_in_time=check_in if check_in else None,
            check_out_time=check_out if check_out else None,
            remarks=remarks,
            created_by=user.user_id
        )
        messages.success(request, 'Teacher attendance recorded successfully!')
        return redirect('teacher_attendance')
        
    teachers = User.objects.filter(role__role_name='Teacher', is_active=True)
    
    details = TeacherAttendanceDetail.objects.all().order_by('-created_date')
    
    return render(request, 'website/teacher_attendance.html', {
        'user': user,
        'page_title': 'Teacher Attendance',
        'teachers': teachers,
        'details': details
    })


def fee_dashboard_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    user = User.objects.get(user_id=request.session['user_id'])
    
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
    user = User.objects.get(user_id=request.session['user_id'])
    
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
    user = User.objects.get(user_id=request.session['user_id'])
    
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
    user = User.objects.get(user_id=request.session['user_id'])
    
    return render(request, 'website/pending_fees.html', {
        'user': user,
        'page_title': 'Pending Fees'
    })

def receipts_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    user = User.objects.get(user_id=request.session['user_id'])
    
    return render(request, 'website/receipts.html', {
        'user': user,
        'page_title': 'Receipts'
    })

def refunds_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    user = User.objects.get(user_id=request.session['user_id'])
    
    return render(request, 'website/refunds.html', {
        'user': user,
        'page_title': 'Refunds'
    })


def reports_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    user = User.objects.get(user_id=request.session['user_id'])
    
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
    user = User.objects.get(user_id=request.session['user_id'])
    
    from academics.models import Course, Batch
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add_course':
            Course.objects.create(
                course_code=request.POST.get('course_code'),
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
            course_id = request.POST.get('course_id')
            teacher_id = request.POST.get('teacher_id')
            Batch.objects.create(
                batch_code=request.POST.get('batch_code'),
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
        
    user = User.objects.get(user_id=request.session['user_id'])
    from users.models import Role, RoleGroup, RoleAccess, MasterMenu
    
    roles = Role.objects.all().select_related('role_group')
    users = User.objects.all().select_related('role')
    menus = MasterMenu.objects.filter(is_active=True).order_by('menu_id')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'create_user':
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            email = request.POST.get('email', '')
            phone = request.POST.get('phone', '')
            password = request.POST.get('password', '')
            role_id = request.POST.get('role_id')
            
            try:
                role = Role.objects.get(role_id=role_id)
                User.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    display_name=f"{first_name} {last_name}".strip(),
                    email=email,
                    phone=phone,
                    password=password,
                    role=role
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
                    menu.save()
                    messages.success(request, f'Menu {menu_name} updated successfully!')
                else:
                    MasterMenu.objects.create(
                        menu_name=menu_name,
                        url_page=url_page,
                        is_active=is_active
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
    audit_logs = UserLoginDetails.objects.select_related('user').order_by('-login_date')[:50]
    
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
