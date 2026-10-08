import re

with open('templates/base.html', 'r') as f:
    content = f.read()

# Student Profile submenus
content = content.replace(
    '<a href="{% url \'students\' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == \'Student Master\' or page_title == \'Student Profile\' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Student Master</a>',
    '{% if user_perms.Student_Master.view or user_perms.Student_Profile.view %}<a href="{% url \'students\' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == \'Student Master\' or page_title == \'Student Profile\' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Student Master</a>{% endif %}'
)
content = content.replace(
    '<a href="{% url \'enrollment_management\' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == \'Enrollment Management\' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Enrollment Management</a>',
    '{% if user_perms.Enrollment_Management.view or user_perms.Student_Profile.view %}<a href="{% url \'enrollment_management\' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == \'Enrollment Management\' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Enrollment Management</a>{% endif %}'
)

# Attendance submenus
content = content.replace(
    '<a href="{% url \'student_attendance\' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == \'Student Attendance\' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Student Attendance</a>',
    '{% if user_perms.Student_Attendance.view or user_perms.Attendance.view %}<a href="{% url \'student_attendance\' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == \'Student Attendance\' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Student Attendance</a>{% endif %}'
)
content = content.replace(
    '<a href="{% url \'teacher_attendance\' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == \'Teacher Attendance\' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Teacher Attendance</a>',
    '{% if user_perms.Teacher_Attendance.view or user_perms.Attendance.view %}<a href="{% url \'teacher_attendance\' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == \'Teacher Attendance\' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Teacher Attendance</a>{% endif %}'
)

# Fees submenus
content = content.replace(
    '<a href="{% url \'fee_dashboard\' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == \'Fee Dashboard\' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Dashboard</a>',
    '{% if user_perms.Fee_Dashboard.view or user_perms.Fees.view %}<a href="{% url \'fee_dashboard\' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == \'Fee Dashboard\' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Dashboard</a>{% endif %}'
)
content = content.replace(
    '<a href="{% url \'assign_fees\' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == \'Assign Fees\' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Assign Fees</a>',
    '{% if user_perms.Assign_Fees.view or user_perms.Fees.view %}<a href="{% url \'assign_fees\' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == \'Assign Fees\' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Assign Fees</a>{% endif %}'
)
content = content.replace(
    '<a href="{% url \'fee_collection\' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == \'Fee Collection\' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Fee Collection</a>',
    '{% if user_perms.Fee_Collection.view or user_perms.Fees.view %}<a href="{% url \'fee_collection\' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == \'Fee Collection\' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Fee Collection</a>{% endif %}'
)
content = content.replace(
    '<a href="{% url \'pending_fees\' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == \'Pending Fees\' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Pending Fees</a>',
    '{% if user_perms.Pending_Fees.view or user_perms.Fees.view %}<a href="{% url \'pending_fees\' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == \'Pending Fees\' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Pending Fees</a>{% endif %}'
)
content = content.replace(
    '<a href="{% url \'receipts\' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == \'Receipts\' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Receipts</a>',
    '{% if user_perms.Receipts.view or user_perms.Fees.view %}<a href="{% url \'receipts\' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == \'Receipts\' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Receipts</a>{% endif %}'
)
content = content.replace(
    '<a href="{% url \'refunds\' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == \'Refunds\' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Refunds</a>',
    '{% if user_perms.Refunds.view or user_perms.Fees.view %}<a href="{% url \'refunds\' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == \'Refunds\' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Refunds</a>{% endif %}'
)
# Note: we used 'Fee Reports' for the db name but the url was url 'reports'. But the sidebar already has url 'reports' as the last fee item, actually no it's in a dropdown.
# Wait, let's look at the actual HTML for fees:
content = content.replace(
    '<a href="{% url \'reports\' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == \'Reports\' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Reports</a>',
    '{% if user_perms.Fee_Reports.view or user_perms.Fees.view %}<a href="{% url \'reports\' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == \'Reports\' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Reports</a>{% endif %}'
)

# Event Scheduling submenus
content = content.replace(
    '<a href="{% url \'events_dashboard\' %}?tab=upcoming" class="block px-4 py-2 text-sm rounded-md {% if active_tab == \'upcoming\' or active_tab == \'list\' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Event List</a>',
    '{% if user_perms.Event_List.view or user_perms.Event_Scheduling.view %}<a href="{% url \'events_dashboard\' %}?tab=upcoming" class="block px-4 py-2 text-sm rounded-md {% if active_tab == \'upcoming\' or active_tab == \'list\' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Event List</a>{% endif %}'
)
content = content.replace(
    '<a href="{% url \'events_dashboard\' %}?tab=registration" class="block px-4 py-2 text-sm rounded-md {% if active_tab == \'registration\' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Event Registration</a>',
    '{% if user_perms.Event_Registration.view or user_perms.Event_Scheduling.view %}<a href="{% url \'events_dashboard\' %}?tab=registration" class="block px-4 py-2 text-sm rounded-md {% if active_tab == \'registration\' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Event Registration</a>{% endif %}'
)
content = content.replace(
    '<a href="{% url \'events_dashboard\' %}?tab=assignments" class="block px-4 py-2 text-sm rounded-md {% if active_tab == \'assignments\' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Teacher Assignments</a>',
    '{% if user_perms.Teacher_Assignments.view or user_perms.Event_Scheduling.view %}<a href="{% url \'events_dashboard\' %}?tab=assignments" class="block px-4 py-2 text-sm rounded-md {% if active_tab == \'assignments\' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Teacher Assignments</a>{% endif %}'
)
content = content.replace(
    '<a href="{% url \'events_dashboard\' %}?tab=venue" class="block px-4 py-2 text-sm rounded-md {% if active_tab == \'venue\' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Venue Management</a>',
    '{% if user_perms.Venue_Management.view or user_perms.Event_Scheduling.view %}<a href="{% url \'events_dashboard\' %}?tab=venue" class="block px-4 py-2 text-sm rounded-md {% if active_tab == \'venue\' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Venue Management</a>{% endif %}'
)
content = content.replace(
    '<a href="{% url \'events_dashboard\' %}?tab=attendance" class="block px-4 py-2 text-sm rounded-md {% if active_tab == \'attendance\' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Event Attendance</a>',
    '{% if user_perms.Event_Attendance.view or user_perms.Event_Scheduling.view %}<a href="{% url \'events_dashboard\' %}?tab=attendance" class="block px-4 py-2 text-sm rounded-md {% if active_tab == \'attendance\' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Event Attendance</a>{% endif %}'
)
content = content.replace(
    '<a href="{% url \'events_dashboard\' %}?tab=reports" class="block px-4 py-2 text-sm rounded-md {% if active_tab == \'reports\' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Event Reports</a>',
    '{% if user_perms.Event_Reports.view or user_perms.Event_Scheduling.view %}<a href="{% url \'events_dashboard\' %}?tab=reports" class="block px-4 py-2 text-sm rounded-md {% if active_tab == \'reports\' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Event Reports</a>{% endif %}'
)

with open('templates/base.html', 'w') as f:
    f.write(content)
