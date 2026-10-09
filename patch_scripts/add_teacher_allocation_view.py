import re

with open('website/views.py', 'r') as f:
    content = f.read()

new_view = """
def teacher_allocation_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
        
    user = User.objects.get(user_id=request.session['user_id'])
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
"""

if "def teacher_allocation_view" not in content:
    with open('website/views.py', 'a') as f:
        f.write(new_view)
