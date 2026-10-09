import re

with open('templates/base.html', 'r') as f:
    content = f.read()

# I will just write a python script to replace the entire <nav id="sidebar-nav" class="flex-1 px-4 py-6 space-y-1 overflow-y-auto"> section!

# Find the start and end of the nav
nav_start = '<nav id="sidebar-nav" class="flex-1 px-4 py-6 space-y-1 overflow-y-auto">'
nav_end_marker = '        </nav>'

start_idx = content.find(nav_start)
end_idx = content.find(nav_end_marker, start_idx) + len(nav_end_marker)

new_nav = """<nav id="sidebar-nav" class="flex-1 px-4 py-6 space-y-1 overflow-y-auto">
            <a href="{% url 'index' %}" class="block px-4 py-2 rounded-md {% if request.resolver_match.url_name == 'index' %}bg-indigo-800 text-white{% else %}hover:bg-indigo-700{% endif %}">Dashboard</a>
            
            {% if user_perms.Student_Profile.view %}
            <div x-data="{ open: {% if 'Student' in page_title or 'Enrollment' in page_title %}true{% else %}false{% endif %} }">
                <button @click="open = !open" class="w-full flex justify-between items-center px-4 py-2 rounded-md hover:bg-indigo-700 focus:outline-none {% if 'Student' in page_title or 'Enrollment' in page_title %}bg-indigo-800 text-white{% endif %}">
                    <span>Student Profile</span>
                    <i class="fa-solid fa-chevron-down text-xs transition-transform duration-200" :class="{'rotate-180': open}"></i>
                </button>
                <div x-show="open" class="pl-4 mt-1 space-y-1">
                    {% if user_perms.Student_Master.view or user_perms.Student_Profile.view %}<a href="{% url 'students' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == 'Student Master' or page_title == 'Student Profile' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Student Master</a>{% endif %}
                    {% if user_perms.Student_Attendance.view or user_perms.Student_Profile.view %}<a href="{% url 'student_attendance' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == 'Student Attendance' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Student Attendance</a>{% endif %}
                </div>
            </div>
            {% endif %}
            
            {% if user_perms.Fees.view %}
            <div x-data="{ open: {% if 'Fee' in page_title or 'Receipts' in page_title or 'Refunds' in page_title or page_title == 'Reports' %}true{% else %}false{% endif %} }">
                <button @click="open = !open" class="w-full flex justify-between items-center px-4 py-2 rounded-md hover:bg-indigo-700 focus:outline-none {% if 'Fee' in page_title or 'Receipts' in page_title or 'Refunds' in page_title or page_title == 'Reports' %}bg-indigo-800 text-white{% endif %}">
                    <span>Fees</span>
                    <i class="fa-solid fa-chevron-down text-xs transition-transform duration-200" :class="{'rotate-180': open}"></i>
                </button>
                <div x-show="open" class="pl-4 mt-1 space-y-1">
                    {% if user_perms.Fee_Dashboard.view or user_perms.Fees.view %}<a href="{% url 'fee_dashboard' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == 'Fee Dashboard' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Dashboard</a>{% endif %}
                    {% if user_perms.Assign_Fees.view or user_perms.Fees.view %}<a href="{% url 'assign_fees' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == 'Assign Fees' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Assign Fees</a>{% endif %}
                    {% if user_perms.Fee_Collection.view or user_perms.Fees.view %}<a href="{% url 'fee_collection' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == 'Fee Collection' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Fee Collection</a>{% endif %}
                    {% if user_perms.Pending_Fees.view or user_perms.Fees.view %}<a href="{% url 'pending_fees' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == 'Pending Fees' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Pending Fees</a>{% endif %}
                    {% if user_perms.Receipts.view or user_perms.Fees.view %}<a href="{% url 'receipts' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == 'Receipts' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Receipts</a>{% endif %}
                    {% if user_perms.Refunds.view or user_perms.Fees.view %}<a href="{% url 'refunds' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == 'Refunds' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Refunds</a>{% endif %}
                    {% if user_perms.Fee_Reports.view or user_perms.Fees.view %}<a href="{% url 'reports' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == 'Reports' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Reports</a>{% endif %}
                </div>
            </div>
            {% endif %}

            {% if user_perms.Event_Scheduling.view %}
            <div x-data="{ open: {% if 'Event' in page_title or 'Venue' in page_title or 'Teacher Assignment' in page_title %}true{% else %}false{% endif %} }">
                <button @click="open = !open" class="w-full flex justify-between items-center px-4 py-2 rounded-md hover:bg-indigo-700 focus:outline-none {% if 'Event' in page_title or 'Venue' in page_title or 'Teacher Assignment' in page_title %}bg-indigo-800 text-white{% endif %}">
                    <span>Event Scheduling</span>
                    <i class="fa-solid fa-chevron-down text-xs transition-transform duration-200" :class="{'rotate-180': open}"></i>
                </button>
                <div x-show="open" class="pl-4 mt-1 space-y-1">
                    {% if user_perms.Event_List.view or user_perms.Event_Scheduling.view %}<a href="{% url 'events_dashboard' %}?tab=upcoming" class="block px-4 py-2 text-sm rounded-md {% if active_tab == 'upcoming' or active_tab == 'list' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Event List</a>{% endif %}
                    {% if user_perms.Event_Registration.view or user_perms.Event_Scheduling.view %}<a href="{% url 'events_dashboard' %}?tab=registration" class="block px-4 py-2 text-sm rounded-md {% if active_tab == 'registration' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Event Registration</a>{% endif %}
                    {% if user_perms.Teacher_Assignments.view or user_perms.Event_Scheduling.view %}<a href="{% url 'events_dashboard' %}?tab=assignments" class="block px-4 py-2 text-sm rounded-md {% if active_tab == 'assignments' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Teacher Assignments</a>{% endif %}
                    {% if user_perms.Venue_Management.view or user_perms.Event_Scheduling.view %}<a href="{% url 'events_dashboard' %}?tab=venue" class="block px-4 py-2 text-sm rounded-md {% if active_tab == 'venue' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Venue Management</a>{% endif %}
                    {% if user_perms.Event_Attendance.view or user_perms.Event_Scheduling.view %}<a href="{% url 'events_dashboard' %}?tab=attendance" class="block px-4 py-2 text-sm rounded-md {% if active_tab == 'attendance' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Event Attendance</a>{% endif %}
                    {% if user_perms.Event_Reports.view or user_perms.Event_Scheduling.view %}<a href="{% url 'events_dashboard' %}?tab=reports" class="block px-4 py-2 text-sm rounded-md {% if active_tab == 'reports' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Event Reports</a>{% endif %}
                </div>
            </div>
            {% endif %}

            {% if user_perms.Courses_and_Batches.view %}
            <a href="{% url 'courses' %}" class="block px-4 py-2 rounded-md {% if page_title == 'Courses & Batches' %}bg-indigo-800 text-white{% else %}hover:bg-indigo-700{% endif %}">Courses & Batches</a>
            {% endif %}
            
            {% if user_perms.Teacher_Profile.view %}
            <div x-data="{ open: {% if 'Teacher' in page_title and not 'Assignment' in page_title %}true{% else %}false{% endif %} }">
                <button @click="open = !open" class="w-full flex justify-between items-center px-4 py-2 rounded-md hover:bg-indigo-700 focus:outline-none {% if 'Teacher' in page_title and not 'Assignment' in page_title %}bg-indigo-800 text-white{% endif %}">
                    <span>Teacher Profile</span>
                    <i class="fa-solid fa-chevron-down text-xs transition-transform duration-200" :class="{'rotate-180': open}"></i>
                </button>
                <div x-show="open" class="pl-4 mt-1 space-y-1">
                    {% if user_perms.Teacher_Master.view or user_perms.Teacher_Profile.view %}<a href="{% url 'teachers' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == 'Teacher Management' or page_title == 'Teacher Master' or page_title == 'Teacher Profile' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Teacher Master</a>{% endif %}
                    {% if user_perms.Teacher_Attendance.view or user_perms.Teacher_Profile.view %}<a href="{% url 'teacher_attendance' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == 'Teacher Attendance' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Teacher Attendance</a>{% endif %}
                </div>
            </div>
            {% endif %}

            <a href="{% url 'timetable' %}" class="block px-4 py-2 rounded-md {% if request.resolver_match.url_name == 'timetable' %}bg-indigo-800 text-white{% else %}hover:bg-indigo-700{% endif %}">Timetable</a>
            <a href="{% url 'generic_page' 'notifications' %}" class="block px-4 py-2 rounded-md {% if page_title == 'Notifications / Reminders' %}bg-indigo-800 text-white{% else %}hover:bg-indigo-700{% endif %}">Notifications</a>
            <a href="{% url 'reports' %}" class="block px-4 py-2 rounded-md {% if page_title == 'Reports' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Reports</a>
            
            <!-- Admin Menu -->
            {% if user_perms.Admin.view %}
            <div x-data="{ open: {% if page_title == 'Admin' %}true{% else %}false{% endif %} }" class="mb-1">
                <button @click="open = !open" class="w-full flex justify-between items-center px-4 py-2 rounded-md {% if page_title == 'Admin' %}bg-indigo-800 text-white{% else %}hover:bg-indigo-700{% endif %} transition-colors">
                    <span>Admin</span>
                    <i :class="open ? 'fa-solid fa-chevron-up text-xs' : 'fa-solid fa-chevron-down text-xs'"></i>
                </button>
                <div x-show="open" x-collapse class="pl-4 pr-2 py-1 space-y-1">
                    {% if user_perms.Admin_Dashboard.view or user_perms.Admin.view %}<a href="{% url 'admin_dashboard' %}?tab=dashboard" class="block px-4 py-1.5 rounded-md text-sm {% if request.GET.tab == 'dashboard' or not request.GET.tab and request.resolver_match.url_name == 'admin_dashboard' %}bg-indigo-600 text-white font-medium{% else %}text-indigo-200 hover:text-white hover:bg-indigo-700/50{% endif %} transition-colors">Dashboard</a>{% endif %}
                    {% if user_perms.User_Management.view or user_perms.Admin.view %}<a href="{% url 'admin_dashboard' %}?tab=users" class="block px-4 py-1.5 rounded-md text-sm {% if request.GET.tab == 'users' %}bg-indigo-600 text-white font-medium{% else %}text-indigo-200 hover:text-white hover:bg-indigo-700/50{% endif %} transition-colors">User Management</a>{% endif %}
                    {% if user_perms.Role_Management.view or user_perms.Admin.view %}<a href="{% url 'admin_dashboard' %}?tab=roles" class="block px-4 py-1.5 rounded-md text-sm {% if request.GET.tab == 'roles' %}bg-indigo-600 text-white font-medium{% else %}text-indigo-200 hover:text-white hover:bg-indigo-700/50{% endif %} transition-colors">Role Management</a>{% endif %}
                    {% if user_perms.Menu_Permissions.view or user_perms.Admin.view %}<a href="{% url 'admin_dashboard' %}?tab=menu" class="block px-4 py-1.5 rounded-md text-sm {% if request.GET.tab == 'menu' %}bg-indigo-600 text-white font-medium{% else %}text-indigo-200 hover:text-white hover:bg-indigo-700/50{% endif %} transition-colors">Menu Permissions</a>{% endif %}
                    {% if user_perms.System_Settings.view or user_perms.Admin.view %}<a href="{% url 'admin_dashboard' %}?tab=settings" class="block px-4 py-1.5 rounded-md text-sm {% if request.GET.tab == 'settings' %}bg-indigo-600 text-white font-medium{% else %}text-indigo-200 hover:text-white hover:bg-indigo-700/50{% endif %} transition-colors">System Settings</a>{% endif %}
                    {% if user_perms.Audit_Logs.view or user_perms.Admin.view %}<a href="{% url 'admin_dashboard' %}?tab=audit" class="block px-4 py-1.5 rounded-md text-sm {% if request.GET.tab == 'audit' %}bg-indigo-600 text-white font-medium{% else %}text-indigo-200 hover:text-white hover:bg-indigo-700/50{% endif %} transition-colors">Audit Logs</a>{% endif %}
                </div>
            </div>
            {% endif %}
            
        </nav>"""

content = content[:start_idx] + new_nav + content[end_idx:]

with open('templates/base.html', 'w') as f:
    f.write(content)
