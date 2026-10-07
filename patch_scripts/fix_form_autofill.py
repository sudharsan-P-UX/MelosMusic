import re

with open('templates/website/admin_dashboard.html', 'r') as f:
    content = f.read()

# Disable form autocomplete
content = content.replace(
    '<form method="POST" action="">',
    '<form method="POST" action="" autocomplete="off">'
)

# Fix email autocomplete
content = content.replace(
    '<input type="email" name="email" required class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-indigo-500 text-sm">',
    '<input type="email" name="email" autocomplete="off" required class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-indigo-500 text-sm">'
)

# Fix password autocomplete
content = content.replace(
    '<input type="password" name="password" required class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-indigo-500 text-sm">',
    '<input type="password" name="password" autocomplete="new-password" required class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-indigo-500 text-sm">'
)

# Fix phone to be 10 digits only
content = content.replace(
    '<input type="text" name="phone" required class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-indigo-500 text-sm">',
    '<input type="text" name="phone" pattern="[0-9]{10}" maxlength="10" minlength="10" title="Phone number must be exactly 10 digits" oninput="this.value = this.value.replace(/[^0-9]/g, \'\')" required autocomplete="off" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-indigo-500 text-sm">'
)

with open('templates/website/admin_dashboard.html', 'w') as f:
    f.write(content)
