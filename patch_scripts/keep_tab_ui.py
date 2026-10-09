import re

with open('templates/website/courses_batches.html', 'r') as f:
    content = f.read()

# Update AlpineJS initialization
old_script = """function courseBatchData() {
    return {
        tab: 'courses',"""

new_script = """function courseBatchData() {
    const urlParams = new URLSearchParams(window.location.search);
    const initialTab = urlParams.get('tab') || 'courses';
    return {
        tab: initialTab,"""

content = content.replace(old_script, new_script)

with open('templates/website/courses_batches.html', 'w') as f:
    f.write(content)
