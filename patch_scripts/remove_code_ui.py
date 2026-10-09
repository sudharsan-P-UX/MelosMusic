import re

with open('templates/website/courses_batches.html', 'r') as f:
    content = f.read()

# Remove the Batch Code div block completely
batch_code_pattern = re.compile(r'<div>\s*<label class="block text-sm font-medium text-gray-700 mb-1">Batch Code</label>\s*<input type="text" name="batch_code" class="w-full border border-gray-200 bg-gray-50 rounded-md px-3 py-2 outline-none text-sm text-gray-500" placeholder="Auto-generated \(e\.g\. B1000\)" readonly>\s*</div>', re.DOTALL)
content = batch_code_pattern.sub('', content)

# Remove the Course Code div block completely (Note: It looks like my previous patch didn't apply Course Code correctly or it was slightly different)
# Let's just use a more general regex for Course Code
course_code_pattern = re.compile(r'<div>\s*<label class="block text-sm font-medium text-gray-700 mb-1">Course Code.*?</label>\s*<input type="text" name="course_code".*?>\s*</div>', re.DOTALL)
content = course_code_pattern.sub('', content)

with open('templates/website/courses_batches.html', 'w') as f:
    f.write(content)
