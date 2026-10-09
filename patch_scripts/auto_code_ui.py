import re

with open('templates/website/courses_batches.html', 'r') as f:
    content = f.read()

# Make Course Code read-only and unrequired
old_course_code = """<label class="block text-sm font-medium text-gray-700 mb-1">Course Code <span class="text-red-500">*</span></label>
                                <input type="text" name="course_code" required class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-1 focus:ring-indigo-500 text-sm" placeholder="e.g. C001">"""
new_course_code = """<label class="block text-sm font-medium text-gray-700 mb-1">Course Code</label>
                                <input type="text" name="course_code" class="w-full border border-gray-200 bg-gray-50 rounded-md px-3 py-2 outline-none text-sm text-gray-500" placeholder="Auto-generated (e.g. C1000)" readonly>"""

content = content.replace(old_course_code, new_course_code)

# Make Batch Code read-only and unrequired
old_batch_code = """<label class="block text-sm font-medium text-gray-700 mb-1">Batch Code <span class="text-red-500">*</span></label>
                                <input type="text" name="batch_code" required class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-1 focus:ring-indigo-500 text-sm" placeholder="e.g. B001">"""
new_batch_code = """<label class="block text-sm font-medium text-gray-700 mb-1">Batch Code</label>
                                <input type="text" name="batch_code" class="w-full border border-gray-200 bg-gray-50 rounded-md px-3 py-2 outline-none text-sm text-gray-500" placeholder="Auto-generated (e.g. B1000)" readonly>"""

content = content.replace(old_batch_code, new_batch_code)

with open('templates/website/courses_batches.html', 'w') as f:
    f.write(content)
