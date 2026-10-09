import re

with open('templates/website/admin_dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove the audit logs tab button
text = re.sub(r'<button @click="tab = \'audit\'".*?>\s*<i class="fa-solid fa-clipboard-list mr-2"></i> Audit Logs\s*</button>', '', text)

# We can leave the audit logs tab content in the file (it just won't be accessible), but to be clean, let's remove it if we can.
# Actually leaving it is harmless since the button is gone, but let's try to remove it.
text = re.sub(r'<!-- Audit Logs Tab -->.*?<div x-show="tab === \'audit\'".*?</div>\n\s*</div>\n\s*</div>', '', text, flags=re.DOTALL)

with open('templates/website/admin_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(text)
