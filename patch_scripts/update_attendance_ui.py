import re

def update_template(filepath, user_type_str):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Remove Add Attendance Button entirely
    add_btn_pattern = r'\{% if menu_access\.add %\}.*?Add Attendance.*?</button>.*?\{% endif %\}'
    content = re.sub(add_btn_pattern, '', content, flags=re.DOTALL)
    
    # Alternatively if not wrapped yet
    add_btn_pattern2 = r'<button[^>]*?Add Attendance.*?</button>'
    content = re.sub(add_btn_pattern2, '', content, flags=re.DOTALL)

    # 2. Update Table Headers
    old_headers = r'<th class="py-3 px-4 font-semibold whitespace-nowrap">Date</th>.*?<th class="py-3 px-4 font-semibold whitespace-nowrap text-center">Actions</th>'
    new_headers = f"""<th class="py-3 px-4 font-semibold whitespace-nowrap">Date (From - To)</th>
                        <th class="py-3 px-4 font-semibold whitespace-nowrap">{user_type_str} Name</th>
                        <th class="py-3 px-4 font-semibold whitespace-nowrap text-center">No Of Days</th>
                        <th class="py-3 px-4 font-semibold whitespace-nowrap text-center">Request Type</th>
                        <th class="py-3 px-4 font-semibold whitespace-nowrap text-center">Status</th>
                        <th class="py-3 px-4 font-semibold whitespace-nowrap text-center">Manager Approval On</th>"""
    
    content = re.sub(old_headers, new_headers, content, flags=re.DOTALL)
    
    # 3. Update Table Rows (for loop)
    old_row = r'\{% for d in details %\}.*?\{% empty %\}'
    new_row = """{% for d in details %}
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
                    {% empty %}"""
    content = re.sub(old_row, new_row, content, flags=re.DOTALL)
    
    # Remove Add Attendance Modal
    modal_pattern = r'<!-- Add Attendance Modal -->.*?<!-- Apply Leave Modal -->'
    content = re.sub(modal_pattern, '<!-- Apply Leave Modal -->', content, flags=re.DOTALL)
    
    # Remove unused colspan in empty state
    content = re.sub(r'<td colspan="8"', '<td colspan="7"', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

update_template('templates/website/student_attendance.html', 'Student')
update_template('templates/website/teacher_attendance.html', 'Teacher')
