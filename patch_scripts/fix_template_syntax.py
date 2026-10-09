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

        html = html.replace('pattern="[0-9]{{{ security_settings.phone_length|default:10 }}}"', 
                            'pattern="[0-9]{{ \'{\' }}{{ security_settings.phone_length|default:10 }}{{ \'}\' }}"')
        
        # In case I used \d variant somewhere
        html = html.replace('pattern="\\d{{{ security_settings.phone_length|default:10 }}}"', 
                            'pattern="\\d{{ \'{\' }}{{ security_settings.phone_length|default:10 }}{{ \'}\' }}"')

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html)
