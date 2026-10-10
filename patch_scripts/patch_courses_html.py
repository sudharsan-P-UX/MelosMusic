import os
import re

def patch_courses_html():
    with open('templates/website/courses_batches.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Add Duration (Hrs) input
    duration_months_html = """<div>
                                <label class="block text-sm font-medium text-gray-700 mb-1">Duration (Months)</label>
                                <input type="number" name="duration_months" class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-1 focus:ring-indigo-500 text-sm">
                            </div>"""
    
    new_duration_html = """<div>
                                <label class="block text-sm font-medium text-gray-700 mb-1">Duration (Months)</label>
                                <input type="number" name="duration_months" class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-1 focus:ring-indigo-500 text-sm">
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-1">Duration (Hrs/Session)</label>
                                <input type="number" step="0.5" name="duration_hrs" class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-1 focus:ring-indigo-500 text-sm" placeholder="e.g. 1.5">
                            </div>"""
    
    if duration_months_html in content:
        content = content.replace(duration_months_html, new_duration_html)
    else:
        print("Could not find duration_months in HTML.")

    with open('templates/website/courses_batches.html', 'w', encoding='utf-8') as f:
        f.write(content)

patch_courses_html()
print("Patched courses_batches.html for Add Course.")
