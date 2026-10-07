import re

files = [
    'templates/website/receipts.html',
    'templates/website/refunds.html',
    'templates/website/pending_fees.html'
]

# For receipts: replace fa-print button
for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()
    
    if 'receipts.html' in filepath:
        content = content.replace(
            '<button class="text-indigo-600 bg-indigo-50 p-1.5 rounded hover:bg-indigo-100"><i class="fa-solid fa-print"></i></button>',
            '<button class="text-indigo-600 bg-indigo-50 p-1.5 rounded hover:bg-indigo-100"><i class="fa-solid fa-print"></i></button>\n                        <button class="text-red-600 bg-red-50 p-1.5 rounded hover:bg-red-100 ml-2"><i class="fa-solid fa-trash-can"></i></button>'
        )
    elif 'refunds.html' in filepath:
        content = content.replace(
            '<button class="text-indigo-600 hover:text-indigo-800" title="View"><i class="fa-regular fa-eye"></i></button>',
            '<button class="text-indigo-600 hover:text-indigo-800" title="View"><i class="fa-regular fa-eye"></i></button>\n                        <button class="text-red-600 hover:text-red-800" title="Delete"><i class="fa-solid fa-trash-can"></i></button>'
        )
    elif 'pending_fees.html' in filepath:
        content = content.replace(
            '<a href="{% url \'fee_collection\' %}" class="text-indigo-600 bg-indigo-50 p-1.5 rounded hover:bg-indigo-100"><i class="fa-solid fa-file-invoice-dollar"></i></a>',
            '<a href="{% url \'fee_collection\' %}" class="text-indigo-600 bg-indigo-50 p-1.5 rounded hover:bg-indigo-100"><i class="fa-solid fa-file-invoice-dollar"></i></a>\n                        <button class="text-red-600 bg-red-50 p-1.5 rounded hover:bg-red-100 ml-2"><i class="fa-solid fa-trash-can"></i></button>'
        )
        
    with open(filepath, 'w') as f:
        f.write(content)
