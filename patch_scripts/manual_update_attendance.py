import re

for filepath in ['templates/website/student_attendance.html', 'templates/website/teacher_attendance.html']:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove button completely
    # Find button manually
    button_start = content.find('<button onclick="openModal()"')
    if button_start == -1:
        button_start = content.find('<button type="button" onclick="openModal()"')
    
    if button_start != -1:
        button_end = content.find('</button>', button_start) + 9
        content = content[:button_start] + content[button_end:]

    # Remove modal completely
    modal_start = content.find('<!-- Add Attendance Modal -->')
    if modal_start != -1:
        modal_end = content.find('<!-- Apply Leave Modal -->')
        if modal_end != -1:
            content = content[:modal_start] + content[modal_end:]

    # Update Table Headers manually
    # Find the <thead>
    thead_start = content.find('<thead')
    thead_end = content.find('</thead>', thead_start)
    old_thead = content[thead_start:thead_end]
    
    user_type_str = 'Student' if 'student' in filepath else 'Teacher'
    new_thead = f"""<thead class="bg-gray-50 border-b border-gray-200 text-gray-700 text-xs uppercase tracking-wider text-left">
                    <tr>
                        <th class="py-3 px-4 font-semibold whitespace-nowrap w-16">#</th>
                        <th class="py-3 px-4 font-semibold whitespace-nowrap">Date (From - To)</th>
                        <th class="py-3 px-4 font-semibold whitespace-nowrap">{user_type_str} Name</th>
                        <th class="py-3 px-4 font-semibold whitespace-nowrap text-center">No Of Days</th>
                        <th class="py-3 px-4 font-semibold whitespace-nowrap text-center">Request Type</th>
                        <th class="py-3 px-4 font-semibold whitespace-nowrap text-center">Status</th>
                        <th class="py-3 px-4 font-semibold whitespace-nowrap text-center">Manager Approval On</th>
                    </tr>"""
    
    content = content.replace(old_thead, new_thead)

    # Update Table Rows manually
    for_start = content.find('{% for d in details %}')
    empty_start = content.find('{% empty %}', for_start)
    old_rows = content[for_start:empty_start]
    
    new_rows = """{% for d in details %}
                    <tr class="border-b border-gray-100 hover:bg-gray-50 transition-colors">
                        <td class="py-3 px-4 text-gray-600">{{ forloop.counter }}</td>
                        <td class="py-3 px-4">{{ d.from_date|date:"d-b-Y" }} to {{ d.to_date|date:"d-b-Y" }}</td>
                        <td class="py-3 px-4 font-medium text-gray-800">{{ d.user.display_name }}</td>
                        <td class="py-3 px-4 text-center">{{ d.no_of_days }}</td>
                        <td class="py-3 px-4 text-center">
                            <span class="px-2.5 py-1 bg-gray-100 text-gray-700 rounded-md text-xs font-medium">{{ d.request_type }}</span>
                        </td>
                        <td class="py-3 px-4 text-center">
                            {% if d.manager_approval_status == 'Approved' %}
                                <span class="px-2.5 py-1 bg-emerald-100 text-emerald-700 rounded-md text-xs font-medium">Approved</span>
                            {% elif d.manager_approval_status == 'Rejected' %}
                                <span class="px-2.5 py-1 bg-red-100 text-red-700 rounded-md text-xs font-medium">Rejected</span>
                            {% else %}
                                <span class="px-2.5 py-1 bg-yellow-100 text-yellow-700 rounded-md text-xs font-medium">Pending</span>
                            {% endif %}
                        </td>
                        <td class="py-3 px-4 text-center text-gray-500 text-sm">
                            {{ d.manager_approval_on|date:"d-b-Y h:i A"|default:"-" }}
                        </td>
                    </tr>
                    """
    content = content.replace(old_rows, new_rows)
    
    # Fix empty state text
    content = content.replace('Click "Add Attendance" to record today\'s attendance.', 'Click "Attendance Request" to submit a new request.')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Done")
