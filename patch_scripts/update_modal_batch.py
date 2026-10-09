import re

def update_modal(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the modal body start
    modal_body_start = r'<div class="p-6 overflow-y-auto flex-1 space-y-4">'
    
    # We will inject the Batch dropdown right after the modal_body_start
    batch_dropdown = """
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Batch <span class="text-red-500">*</span></label>
                    <select name="batch_id" required class="w-full border-gray-300 rounded-md shadow-sm focus:ring-purple-500 focus:border-purple-500 text-sm">
                        <option value="">Select Batch</option>
                        {% for b in allocated_batches %}
                            <option value="{{ b.batch_id }}">{{ b.batch_name }}</option>
                        {% endfor %}
                    </select>
                    {% if not allocated_batches %}
                        <p class="text-xs text-red-500 mt-1"><i class="fa-solid fa-circle-exclamation mr-1"></i> You are not allocated to any batches. You cannot submit an attendance request.</p>
                    {% endif %}
                </div>"""
                
    content = content.replace(modal_body_start, modal_body_start + batch_dropdown)
    
    # Disable the submit button if allocated_batches is empty
    submit_btn = r'<button type="submit" class="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 font-medium text-sm transition shadow-sm">'
    disabled_submit_btn = """<button type="submit" {% if not allocated_batches %}disabled class="px-4 py-2 bg-gray-400 text-white rounded-md font-medium text-sm transition shadow-sm cursor-not-allowed"{% else %}class="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 font-medium text-sm transition shadow-sm"{% endif %}>"""
    
    content = content.replace(submit_btn, disabled_submit_btn)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

update_modal('templates/website/student_attendance_v2.html')
update_modal('templates/website/teacher_attendance_v2.html')
