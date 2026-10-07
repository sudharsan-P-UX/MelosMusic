import re

with open('templates/base.html', 'r') as f:
    content = f.read()

# 1. Student Profile parent
content = content.replace(
    "{% if page_title == 'Student Profile' %}bg-indigo-800 text-white{% endif %}",
    "{% if page_title == 'Student Master' or page_title == 'Enrollment Management' %}bg-indigo-800 text-white{% endif %}"
)

# 2. Student Profile children
content = content.replace(
    "{% if page_title == 'Student Master' %}bg-indigo-800 text-white{% else %}hover:bg-indigo-700{% endif %}",
    "{% if page_title == 'Student Master' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}"
)
content = content.replace(
    "{% if page_title == 'Enrollment Management' %}bg-indigo-800 text-white{% else %}hover:bg-indigo-700{% endif %}",
    "{% if page_title == 'Enrollment Management' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}"
)

# 3. Attendance parent is fine: {% if 'Attendance' in page_title %}

# 4. Attendance children
content = content.replace(
    "{% if page_title == 'Student Attendance' %}bg-indigo-800 text-white{% else %}hover:bg-indigo-700{% endif %}",
    "{% if page_title == 'Student Attendance' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}"
)
content = content.replace(
    "{% if page_title == 'Teacher Attendance' %}bg-indigo-800 text-white{% else %}hover:bg-indigo-700{% endif %}",
    "{% if page_title == 'Teacher Attendance' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}"
)

# 5. Fees parent is fine: {% if 'Fee' in page_title or 'Receipt' in page_title or 'Refund' in page_title %}

# 6. Fees children
fee_tabs = ['Fee Dashboard', 'Assign Fees', 'Fee Collection', 'Pending Fees', 'Receipts', 'Refunds', 'Reports']
for tab in fee_tabs:
    content = content.replace(
        f"{{% if page_title == '{tab}' %}}bg-indigo-800 text-white{{% else %}}hover:bg-indigo-700{{% endif %}}",
        f"{{% if page_title == '{tab}' %}}bg-indigo-600 text-white font-medium{{% else %}}hover:bg-indigo-700{{% endif %}}"
    )

with open('templates/base.html', 'w') as f:
    f.write(content)
