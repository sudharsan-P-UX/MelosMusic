import re

with open('templates/website/attendance_log.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add Actions column header
content = content.replace('<th class="py-3 px-4 font-semibold whitespace-nowrap text-center">Status</th>', 
                          '<th class="py-3 px-4 font-semibold whitespace-nowrap text-center">Status</th>\n                        <th class="py-3 px-4 font-semibold whitespace-nowrap text-center">Action</th>')

# Add Actions button
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
                            {% if l.manager_approval_status != 'Pending' %}
                            <form method="POST" action="?tab={{ tab }}" class="flex items-center justify-center">
                                {% csrf_token %}
                                <input type="hidden" name="leave_request_id" value="{{ l.leave_request_id }}">
                                <button type="submit" name="action" value="Revoke" class="bg-gray-100 text-gray-600 hover:bg-red-500 hover:text-white px-3 py-1 rounded-md text-xs font-medium transition-colors" title="Revoke Decision">
                                    <i class="fa-solid fa-rotate-left mr-1"></i> Revoke
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

with open('templates/website/attendance_log.html', 'w', encoding='utf-8') as f:
    f.write(content)
