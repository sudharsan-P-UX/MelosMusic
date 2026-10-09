import os
import re

files = [
    'templates/website/admin_dashboard.html',
    'templates/website/students.html',
    'templates/website/teachers.html'
]

for file_path in files:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            html = f.read()

        # Phone logic
        # Remove hardcoded length limits and pattern
        html = re.sub(r'maxlength="10"', 'maxlength="{{ security_settings.phone_length|default:10 }}"', html)
        html = re.sub(r'minlength="10"', 'minlength="{{ security_settings.phone_length|default:10 }}"', html)
        html = re.sub(r'pattern="\[0-9\]\{10\}"', 'pattern="[0-9]{{{ security_settings.phone_length|default:10 }}}"', html)
        html = re.sub(r'pattern="\\d\{10\}"', 'pattern="\\\\d{{{ security_settings.phone_length|default:10 }}}"', html)
        html = re.sub(r'title="Phone number must be exactly 10 digits"', 'title="Phone number must be exactly {{ security_settings.phone_length|default:10 }} digits"', html)

        # Email logic
        # Add maxlength
        html = re.sub(r'(name="email"(?!.*?maxlength))', r'\1 maxlength="{{ security_settings.email_length|default:255 }}"', html)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html)
