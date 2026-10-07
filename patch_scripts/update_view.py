with open('templates/website/teachers.html', 'r') as f:
    content = f.read()

action_buttons = '''
                        <!-- View Button -->
                        <button onclick="document.getElementById('viewModal_{{ teacher.user_id }}').classList.remove('hidden'); document.getElementById('viewModal_{{ teacher.user_id }}').classList.add('flex');" class="text-green-600 hover:text-green-900 transition" title="View">
                            <i class="fa-solid fa-eye"></i>
                        </button>
                        <!-- Update Button -->
'''
content = content.replace('<!-- Update Button -->', action_buttons)

view_modal_template = '''
                {% empty %}
'''

view_modal = '''
                <!-- View Modal for this teacher -->
                <div id="viewModal_{{ teacher.user_id }}" class="fixed inset-0 bg-gray-900 bg-opacity-50 hidden items-center justify-center z-50 transition-opacity">
                    <div class="bg-white rounded-lg shadow-xl w-full max-w-4xl mx-4 overflow-hidden flex flex-col max-h-[90vh]">
                        <div class="px-6 py-4 border-b border-gray-200 flex justify-between items-center bg-gray-50 flex-shrink-0">
                            <h3 class="text-lg font-bold text-gray-800">Teacher Details: {{ teacher.display_name }}</h3>
                            <button type="button" onclick="document.getElementById('viewModal_{{ teacher.user_id }}').classList.add('hidden'); document.getElementById('viewModal_{{ teacher.user_id }}').classList.remove('flex');" class="text-gray-400 hover:text-gray-600">
                                <i class="fa-solid fa-xmark text-xl"></i>
                            </button>
                        </div>
                        <div class="p-6 overflow-y-auto space-y-6">
                            <!-- Personal Info -->
                            <div>
                                <h4 class="text-md font-bold text-gray-800 border-b pb-2 mb-3">Personal Information</h4>
                                <div class="grid grid-cols-2 gap-4 text-sm">
                                    <div><span class="font-medium text-gray-500">Name:</span> {{ teacher.display_name }}</div>
                                    <div><span class="font-medium text-gray-500">Email:</span> {{ teacher.email }}</div>
                                    <div><span class="font-medium text-gray-500">Phone:</span> {{ teacher.phone }}</div>
                                    <div><span class="font-medium text-gray-500">Status:</span> {% if teacher.is_active %}Active{% else %}Inactive{% endif %}</div>
                                </div>
                            </div>
                            
                            <!-- Qualifications -->
                            <div>
                                <h4 class="text-md font-bold text-gray-800 border-b pb-2 mb-3">Educational Qualifications</h4>
                                {% if teacher.qualifications.all %}
                                <table class="min-w-full bg-white border border-gray-200">
                                    <thead class="bg-gray-50 text-gray-600 text-xs text-left">
                                        <tr>
                                            <th class="py-2 px-3">Institution</th>
                                            <th class="py-2 px-3">Qualification</th>
                                            <th class="py-2 px-3">Passed Year</th>
                                            <th class="py-2 px-3">GPA/CGPA</th>
                                        </tr>
                                    </thead>
                                    <tbody class="text-sm divide-y divide-gray-200">
                                        {% for q in teacher.qualifications.all %}
                                        <tr>
                                            <td class="py-2 px-3">{{ q.institution }}</td>
                                            <td class="py-2 px-3">{{ q.qualification }}</td>
                                            <td class="py-2 px-3">{{ q.passed_year }}</td>
                                            <td class="py-2 px-3">{{ q.gpa }}</td>
                                        </tr>
                                        {% endfor %}
                                    </tbody>
                                </table>
                                {% else %}
                                <p class="text-sm text-gray-500">No qualifications recorded.</p>
                                {% endif %}
                            </div>

                            <!-- Experience -->
                            <div>
                                <h4 class="text-md font-bold text-gray-800 border-b pb-2 mb-3">Experience</h4>
                                {% if teacher.experiences.all %}
                                <table class="min-w-full bg-white border border-gray-200">
                                    <thead class="bg-gray-50 text-gray-600 text-xs text-left">
                                        <tr>
                                            <th class="py-2 px-3">Company</th>
                                            <th class="py-2 px-3">Role</th>
                                            <th class="py-2 px-3">From</th>
                                            <th class="py-2 px-3">To</th>
                                            <th class="py-2 px-3">Years</th>
                                        </tr>
                                    </thead>
                                    <tbody class="text-sm divide-y divide-gray-200">
                                        {% for e in teacher.experiences.all %}
                                        <tr>
                                            <td class="py-2 px-3">{{ e.company_name }}</td>
                                            <td class="py-2 px-3">{{ e.role }}</td>
                                            <td class="py-2 px-3">{{ e.from_date|date:"Y-m-d" }}</td>
                                            <td class="py-2 px-3">{{ e.to_date|date:"Y-m-d" }}</td>
                                            <td class="py-2 px-3">{{ e.years_of_experience }}</td>
                                        </tr>
                                        {% endfor %}
                                    </tbody>
                                </table>
                                {% else %}
                                <p class="text-sm text-gray-500">No experience recorded.</p>
                                {% endif %}
                            </div>
                            
                            <!-- Certifications -->
                            <div>
                                <h4 class="text-md font-bold text-gray-800 border-b pb-2 mb-3">Certifications</h4>
                                {% if teacher.certifications.all %}
                                <table class="min-w-full bg-white border border-gray-200">
                                    <thead class="bg-gray-50 text-gray-600 text-xs text-left">
                                        <tr>
                                            <th class="py-2 px-3">Certificate Name</th>
                                            <th class="py-2 px-3">Year</th>
                                            <th class="py-2 px-3">Document</th>
                                        </tr>
                                    </thead>
                                    <tbody class="text-sm divide-y divide-gray-200">
                                        {% for c in teacher.certifications.all %}
                                        <tr>
                                            <td class="py-2 px-3">{{ c.certificate_name }}</td>
                                            <td class="py-2 px-3">{{ c.year }}</td>
                                            <td class="py-2 px-3">
                                                {% if c.document %}
                                                <a href="{{ c.document.url }}" target="_blank" class="text-indigo-600 hover:underline">View Document</a>
                                                {% else %}
                                                <span class="text-gray-400">None</span>
                                                {% endif %}
                                            </td>
                                        </tr>
                                        {% endfor %}
                                    </tbody>
                                </table>
                                {% else %}
                                <p class="text-sm text-gray-500">No certifications recorded.</p>
                                {% endif %}
                            </div>
                        </div>
                    </div>
                </div>
                
                {% empty %}
'''

content = content.replace(view_modal_template, view_modal)

with open('templates/website/teachers.html', 'w') as f:
    f.write(content)
