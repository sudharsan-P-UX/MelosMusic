import re
with open('templates/website/courses_batches.html', 'r') as f:
    content = f.read()

# Make the modal box flex col with max height
content = content.replace(
    'class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl w-full"',
    'class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl w-full flex flex-col max-h-[90vh]"'
)

# Make the body scrollable
content = content.replace(
    'class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4 border-b border-gray-200"',
    'class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4 border-b border-gray-200 overflow-y-auto flex-1"'
)

with open('templates/website/courses_batches.html', 'w') as f:
    f.write(content)
