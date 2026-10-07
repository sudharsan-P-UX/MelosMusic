with open('templates/base.html', 'r') as f:
    content = f.read()

import re

# Remove Student Fees and Student Reports
content = re.sub(r'<a href="{% url \'fee_dashboard\' %}" class="block px-4 py-2 text-sm rounded-md hover:bg-indigo-700">Student Fees</a>\s*', '', content)
content = re.sub(r'<a href="{% url \'reports\' %}" class="block px-4 py-2 text-sm rounded-md hover:bg-indigo-700">Student Reports</a>\s*', '', content)

with open('templates/base.html', 'w') as f:
    f.write(content)
