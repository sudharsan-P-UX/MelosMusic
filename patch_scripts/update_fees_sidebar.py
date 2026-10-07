with open('templates/base.html', 'r') as f:
    content = f.read()

old_fees = '''            <a href="{% url 'generic_page' 'fees' %}" class="block px-4 py-2 rounded-md {% if page_title == 'Fees' %}bg-indigo-800 text-white{% else %}hover:bg-indigo-700{% endif %}">Fees</a>'''

new_fees = '''            <div x-data="{ open: {% if 'Fee' in page_title or 'Receipt' in page_title or 'Refund' in page_title %}true{% else %}false{% endif %} }">
                <button @click="open = !open" class="w-full flex justify-between items-center px-4 py-2 rounded-md hover:bg-indigo-700 focus:outline-none">
                    <span>Fees</span>
                    <i class="fa-solid fa-chevron-down text-xs transition-transform duration-200" :class="{'rotate-180': open}"></i>
                </button>
                <div x-show="open" class="pl-4 mt-1 space-y-1">
                    <a href="{% url 'fee_dashboard' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == 'Fee Dashboard' %}bg-indigo-800 text-white{% else %}hover:bg-indigo-700{% endif %}">Dashboard</a>
                    <a href="{% url 'generic_page' 'assign-fees' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == 'Assign Fees' %}bg-indigo-800 text-white{% else %}hover:bg-indigo-700{% endif %}">Assign Fees</a>
                    <a href="{% url 'generic_page' 'fee-collection' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == 'Fee Collection' %}bg-indigo-800 text-white{% else %}hover:bg-indigo-700{% endif %}">Fee Collection</a>
                    <a href="{% url 'generic_page' 'pending-fees' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == 'Pending Fees' %}bg-indigo-800 text-white{% else %}hover:bg-indigo-700{% endif %}">Pending Fees</a>
                    <a href="{% url 'generic_page' 'receipts' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == 'Receipts' %}bg-indigo-800 text-white{% else %}hover:bg-indigo-700{% endif %}">Receipts</a>
                    <a href="{% url 'generic_page' 'refunds' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == 'Refunds' %}bg-indigo-800 text-white{% else %}hover:bg-indigo-700{% endif %}">Refunds</a>
                    <a href="{% url 'generic_page' 'reports' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == 'Reports' %}bg-indigo-800 text-white{% else %}hover:bg-indigo-700{% endif %}">Reports</a>
                </div>
            </div>'''
            
content = content.replace(old_fees, new_fees)

with open('templates/base.html', 'w') as f:
    f.write(content)
