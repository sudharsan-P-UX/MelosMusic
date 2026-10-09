import re

with open('templates/website/student_course.html', 'r') as f:
    content = f.read()

# 1. Remove Add button
add_btn_pattern = re.compile(r'<button @click="showModal = true".*?</button>', re.DOTALL)
content = add_btn_pattern.sub('', content)

# 2. Remove Modal and Script
modal_pattern = re.compile(r'<!-- Allocation Modal -->.*?</script>', re.DOTALL)
content = modal_pattern.sub('', content)

# 3. Rename Header
content = content.replace('{% block header %}Student Course Allocation{% endblock %}', '{% block header %}Allocation Details{% endblock %}')
content = content.replace('Student Course Allocations', 'Allocation Details')

with open('templates/website/student_course.html', 'w') as f:
    f.write(content)
