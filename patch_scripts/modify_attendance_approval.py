import re

with open('templates/website/attendance_approval.html', 'r') as f:
    content = f.read()

# Update Title
content = content.replace('Attendance Log', 'Attendance Approval')
# Update default filter dropdown
old_select = """<select name="filter_status" class="border border-gray-300 rounded px-2 py-1.5 text-sm focus:outline-none focus:ring-1 focus:border-[#5c4b99] bg-white">
                    <option value="">All Statuses</option>
                    <option value="Pending" {% if request.GET.filter_status == 'Pending' %}selected{% endif %}>Pending</option>
                    <option value="Approved" {% if request.GET.filter_status == 'Approved' %}selected{% endif %}>Approved</option>
                    <option value="Rejected" {% if request.GET.filter_status == 'Rejected' %}selected{% endif %}>Rejected</option>
                </select>"""
                
new_select = """<select name="filter_status" class="border border-gray-300 rounded px-2 py-1.5 text-sm focus:outline-none focus:ring-1 focus:border-[#5c4b99] bg-white">
                    <option value="">All Statuses</option>
                    <option value="Pending" {% if request.GET.filter_status == 'Pending' or not request.GET.filter_status %}selected{% endif %}>Pending</option>
                    <option value="Approved" {% if request.GET.filter_status == 'Approved' %}selected{% endif %}>Approved</option>
                    <option value="Rejected" {% if request.GET.filter_status == 'Rejected' %}selected{% endif %}>Rejected</option>
                </select>"""
content = content.replace(old_select, new_select)

# Add Actions column header
content = content.replace('<th class="py-3 px-4 font-semibold whitespace-nowrap text-center">Status</th>', 
                          '<th class="py-3 px-4 font-semibold whitespace-nowrap text-center">Status</th>\n                        <th class="py-3 px-4 font-semibold whitespace-nowrap text-center">Actions</th>')

# Add Actions buttons
old_td = """                        <td class="py-3 px-4 text-center">
                            {% if l.manager_approval_status == 'Approved' %}
                                <span class="px-2.5 py-1 bg-emerald-100 text-emerald-700 rounded-md text-xs font-medium">Approved</span>
                            {% elif l.manager_approval_status == 'Rejected' %}
                                <span class="px-2.5 py-1 bg-red-100 text-red-700 rounded-md text-xs font-medium">Rejected</span>
                            {% else %}
                                <span class="px-2.5 py-1 bg-yellow-100 text-yellow-700 rounded-md text-xs font-medium">Pending</span>
                            {% endif %}
                        </td>
                    </tr>"""
                    
new_td = """                        <td class="py-3 px-4 text-center">
                            {% if l.manager_approval_status == 'Approved' %}
                                <span class="px-2.5 py-1 bg-emerald-100 text-emerald-700 rounded-md text-xs font-medium">Approved</span>
                            {% elif l.manager_approval_status == 'Rejected' %}
                                <span class="px-2.5 py-1 bg-red-100 text-red-700 rounded-md text-xs font-medium">Rejected</span>
                            {% else %}
                                <span class="px-2.5 py-1 bg-yellow-100 text-yellow-700 rounded-md text-xs font-medium">Pending</span>
                            {% endif %}
                        </td>
                        <td class="py-3 px-4 text-center">
                            {% if l.manager_approval_status == 'Pending' %}
                            <form method="POST" action="?tab={{ tab }}" class="flex items-center justify-center space-x-2">
                                {% csrf_token %}
                                <input type="hidden" name="leave_request_id" value="{{ l.leave_request_id }}">
                                <button type="submit" name="action" value="Approve" class="bg-emerald-50 text-emerald-600 hover:bg-emerald-600 hover:text-white px-2.5 py-1 rounded-md text-xs font-medium transition-colors" title="Accept">
                                    <i class="fa-solid fa-check"></i>
                                </button>
                                <button type="submit" name="action" value="Reject" class="bg-red-50 text-red-600 hover:bg-red-600 hover:text-white px-2.5 py-1 rounded-md text-xs font-medium transition-colors" title="Reject">
                                    <i class="fa-solid fa-xmark"></i>
                                </button>
                            </form>
                            {% else %}
                            <span class="text-gray-300">-</span>
                            {% endif %}
                        </td>
                    </tr>"""
content = content.replace(old_td, new_td)

# Fix empty colspan
content = content.replace('<td colspan="8" class="py-8 text-center text-gray-500">', '<td colspan="9" class="py-8 text-center text-gray-500">')

with open('templates/website/attendance_approval.html', 'w') as f:
    f.write(content)
