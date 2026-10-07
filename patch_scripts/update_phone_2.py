for filename in ['templates/website/students.html', 'templates/website/teachers.html']:
    with open(filename, 'r') as f:
        content = f.read()
    
    old_phone = '<input type="text" id="modalPhone" name="phone" oninput="this.value = this.value.replace(/[^0-9]/g, \'\')"'
    new_phone = '<input type="text" id="modalPhone" name="phone" oninput="this.value = this.value.replace(/[^0-9]/g, \'\')" maxlength="10" minlength="10" pattern="\\d{10}" title="Phone number must be exactly 10 digits"'
    content = content.replace(old_phone, new_phone)
    
    with open(filename, 'w') as f:
        f.write(content)
