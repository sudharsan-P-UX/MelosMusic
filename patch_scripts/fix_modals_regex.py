import re

with open('templates/website/courses_batches.html', 'r') as f:
    content = f.read()

# Replace Course Modal wrapper
course_pattern = re.compile(r'<!-- Add Course Modal -->.*?<form method="POST"', re.DOTALL)
course_replacement = '''<!-- Add Course Modal -->
    <div x-show="showCourseModal" style="display: none;" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
        <div @click.away="showCourseModal = false" class="bg-white rounded-lg text-left overflow-hidden shadow-xl w-full max-w-2xl flex flex-col max-h-[90vh]">
            <form method="POST"'''
content = course_pattern.sub(course_replacement, content)

# Replace Batch Modal wrapper
batch_pattern = re.compile(r'<!-- Add Batch Modal -->.*?<form method="POST"', re.DOTALL)
batch_replacement = '''<!-- Add Batch Modal -->
    <div x-show="showBatchModal" style="display: none;" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
        <div @click.away="showBatchModal = false" class="bg-white rounded-lg text-left overflow-hidden shadow-xl w-full max-w-2xl flex flex-col max-h-[90vh]">
            <form method="POST"'''
content = batch_pattern.sub(batch_replacement, content)

# Remove the extra ending divs since we removed 2 divs from the start of each modal
# Each modal had 4 closing divs after </form>. We need only 2.
# But it's safer to just let the browser auto-close them if they are dangling, or we can precisely match the end.
# The end looks like:
# </form>
#             </div>
#         </div>
#     </div>

end_pattern = re.compile(r'</form>\s*</div>\s*</div>\s*</div>')
end_replacement = '''</form>
        </div>
    </div>'''
content = end_pattern.sub(end_replacement, content)

with open('templates/website/courses_batches.html', 'w') as f:
    f.write(content)
print("Modals fixed successfully.")
