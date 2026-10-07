import re

with open('templates/base.html', 'r') as f:
    content = f.read()

# Fix Student Profile Parent Button
content = content.replace(
    '<button @click="open = !open" class="w-full flex justify-between items-center px-4 py-2 rounded-md hover:bg-indigo-700 focus:outline-none">',
    '<button @click="open = !open" class="w-full flex justify-between items-center px-4 py-2 rounded-md hover:bg-indigo-700 focus:outline-none {% if page_title == \'Student Profile\' or page_title == \'Enrollment Management\' %}bg-indigo-800 text-white{% endif %}">',
    1 # Only the first one, which is Student Profile
)

# Fix Student Master Submenu
content = content.replace(
    "{% if page_title == 'Student Master' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}",
    "{% if page_title == 'Student Profile' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}"
)

# Wait, in the earlier step I used `page_title == 'Student Master' or page_title == 'Enrollment Management'` for the parent?
# Let's clean up any previous messes for the parent just in case.
content = re.sub(
    r'<button @click="open = !open" class="w-full flex justify-between items-center px-4 py-2 rounded-md hover:bg-indigo-700 focus:outline-none \{% if page_title == \'Student Master\'.*?%\}.*?\{% endif %\}">',
    '<button @click="open = !open" class="w-full flex justify-between items-center px-4 py-2 rounded-md hover:bg-indigo-700 focus:outline-none {% if page_title == \'Student Profile\' or page_title == \'Enrollment Management\' %}bg-indigo-800 text-white{% endif %}">',
    content
)

# Wait, what does the Student Profile parent look like exactly right now?
