import os
import re

def fix_template(filepath, user_type):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Remove Add Attendance Button
    content = re.sub(r'<button onclick="openModal\(\)".*?Add Attendance\s*</button>', '', content, flags=re.DOTALL)
    
    # 2. Update Headers
    old_thead = r'<thead class="bg-gray-50 border-b border-gray-200 text-gray-700 text-xs uppercase tracking-wider text-left">.*?</thead>'
    new_thead = f"""<thead class="bg-gray-50 border-b border-gray-200 text-gray-700 text-xs uppercase tracking-wider text-left">
                  <tr>
                      <th class="py-3 px-4 font-semibold whitespace-nowrap w-16">#</th>
                      <th class="py-3 px-4 font-semibold whitespace-nowrap">Date (From - To)</th>
                      <th class="py-3 px-4 font-semibold whitespace-nowrap">{user_type} Name</th>
                      <th class="py-3 px-4 font-semibold whitespace-nowrap text-center">No Of Days</th>
                      <th class="py-3 px-4 font-semibold whitespace-nowrap text-center">Request Type</th>
                      <th class="py-3 px-4 font-semibold whitespace-nowrap text-center">Status</th>
                      <th class="py-3 px-4 font-semibold whitespace-nowrap text-center">Manager Approval On</th>
                  </tr>
              </thead>"""
    content = re.sub(old_thead, new_thead, content, flags=re.DOTALL)
    
    # 3. Update Rows
    old_tbody = r'{% for d in details %}.*?{% empty %}'
    new_tbody = """{% for d in details %}
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
    content = re.sub(old_tbody, new_tbody, content, flags=re.DOTALL)
    
    # 4. Remove Add Attendance Modal completely
    content = re.sub(r'<!-- Add Attendance Modal -->.*?<!-- Attendance Request Modal -->', '<!-- Attendance Request Modal -->', content, flags=re.DOTALL)
    
    # 5. Fix empty state message and colspans
    content = content.replace('Click "Add Attendance" to record today\'s attendance.', 'Click "Attendance Request" to submit a new request.')
    content = content.replace('<td colspan="8"', '<td colspan="7"')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# We need to manually fix student_attendance since git checkout failed due to lock
# But first try to unlock it and checkout
import subprocess
try:
    # Try closing any rogue python processes holding it, then checkout
    subprocess.run(['git', 'checkout', 'templates/website/student_attendance.html'])
except:
    pass

fix_template('templates/website/student_attendance.html', 'Student')
fix_template('templates/website/teacher_attendance.html', 'Teacher')
print("Fix applied successfully!")
