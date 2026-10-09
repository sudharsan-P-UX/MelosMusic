import re

with open('templates/website/admin_dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Add form start
bad1 = """<div class="bg-white rounded border border-gray-200 shadow-sm p-6">
            <h3 class="font-medium text-gray-800 mb-6 pb-2 border-b border-gray-100">General Configuration</h3>"""
good1 = """<div class="bg-white rounded border border-gray-200 shadow-sm p-6">
            <form method="POST" action="">
            {% csrf_token %}
            <input type="hidden" name="action" value="save_settings">
            <h3 class="font-medium text-gray-800 mb-6 pb-2 border-b border-gray-100">General Configuration</h3>"""

# Add form end
bad2 = """            <div class="mt-8 flex justify-end">
                <button class="bg-[#4f46e5] text-white px-6 py-2 rounded text-sm font-medium hover:bg-indigo-700 shadow-sm transition">
                    Save Settings
                </button>
            </div>
        </div>"""
good2 = """            <div class="mt-8 flex justify-end">
                <button type="submit" class="bg-[#4f46e5] text-white px-6 py-2 rounded text-sm font-medium hover:bg-indigo-700 shadow-sm transition">
                    Save Settings
                </button>
            </div>
            </form>
        </div>"""

# Add name attributes and bind values
text = text.replace('value="10"', 'name="phone_length" value="{{ security_settings.phone_length|default:10 }}"')
text = text.replace('value="255"', 'name="email_length" value="{{ security_settings.email_length|default:255 }}"')
text = text.replace('value="90"', 'name="password_expire" value="{{ security_settings.password_expire|default:90 }}"')

text = text.replace(bad1, good1)
text = text.replace(bad2, good2)

with open('templates/website/admin_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(text)
