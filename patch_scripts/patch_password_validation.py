import os
import re

def patch_template(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Update form tag to handle client-side password validation
    # Both students and teachers use <form id="[student/teacher]Form" method="POST" ...>
    # We will just inject x-data and @submit to any form that has POST inside the modal
    text = re.sub(
        r'<form (id=".*?Form" method="POST" action=".*?">)',
        r'<form \1 x-data="{ passwordError: false }" @submit="if(document.getElementById(\'modalPassword\').value !== document.getElementById(\'modalConfirmPassword\').value) { $event.preventDefault(); passwordError = true; } else { passwordError = false; }">',
        text
    )
    
    # 2. Add show password eye icon for modalPassword
    password_input = r'<input type="password" id="modalPassword" name="password" class="(.*?)" autocomplete="new-password">'
    password_replacement = r"""<div class="relative" x-data="{ show: false }">
                            <input :type="show ? 'text' : 'password'" id="modalPassword" name="password" class="\1 pr-10" autocomplete="new-password">
                            <button type="button" @click="show = !show" class="absolute inset-y-0 right-0 px-3 flex items-center text-gray-500 hover:text-indigo-600 focus:outline-none">
                                <i class="fa-solid" :class="show ? 'fa-eye-slash' : 'fa-eye'"></i>
                            </button>
                        </div>"""
    text = re.sub(password_input, password_replacement, text)

    # 3. Add show password eye icon for modalConfirmPassword AND the error message
    confirm_input = r'<input type="password" id="modalConfirmPassword" name="confirm_password" class="(.*?)" autocomplete="new-password">'
    confirm_replacement = r"""<div class="relative" x-data="{ show: false }">
                            <input :type="show ? 'text' : 'password'" id="modalConfirmPassword" name="confirm_password" class="\1 pr-10" autocomplete="new-password">
                            <button type="button" @click="show = !show" class="absolute inset-y-0 right-0 px-3 flex items-center text-gray-500 hover:text-indigo-600 focus:outline-none">
                                <i class="fa-solid" :class="show ? 'fa-eye-slash' : 'fa-eye'"></i>
                            </button>
                        </div>
                        <p x-show="passwordError" x-cloak style="display: none;" class="text-red-500 text-xs mt-1 font-medium"><i class="fa-solid fa-circle-exclamation mr-1"></i> Passwords do not match!</p>"""
    text = re.sub(confirm_input, confirm_replacement, text)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

patch_template('templates/website/students.html')
patch_template('templates/website/teachers.html')
print("Password validation and toggle icons added.")
