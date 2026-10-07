import re

with open('templates/website/teachers.html', 'r') as f:
    content = f.read()

old_form_start = """        <div class="p-6 overflow-y-auto">
            <form id="teacherForm" method="POST" action="{% url 'teachers' %}" enctype="multipart/form-data" class="space-y-4" autocomplete="off">"""
new_form_start = """        <form id="teacherForm" method="POST" action="{% url 'teachers' %}" enctype="multipart/form-data" class="flex flex-col flex-1 overflow-hidden" autocomplete="off">
            <div class="p-6 overflow-y-auto space-y-4 flex-1">"""
content = content.replace(old_form_start, new_form_start)

old_form_end = """                <div class="mt-6 flex justify-end space-x-3 pt-4 border-t">
                    <button type="button" onclick="closeModal()" class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 transition">Cancel</button>
                    <button type="submit" id="modalSubmitBtn" class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 shadow transition">Save Teacher</button>
                </div>
            </form>
        </div>"""
new_form_end = """            </div>
            <div class="px-6 py-4 border-t bg-gray-50 flex justify-end space-x-3 flex-shrink-0">
                <button type="button" onclick="closeModal()" class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 transition">Cancel</button>
                <button type="submit" id="modalSubmitBtn" class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 shadow transition">Save Teacher</button>
            </div>
        </form>"""
content = content.replace(old_form_end, new_form_end)

# Also phone number only integer
old_phone = '<input type="text" id="modalPhone" name="phone"'
new_phone = '<input type="number" id="modalPhone" name="phone"'
content = content.replace(old_phone, new_phone)

# Also add eye icon to password fields
old_password = """                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
                        <input type="password" id="modalPassword" name="password" class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-2 focus:ring-indigo-500" autocomplete="new-password">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Confirm Password</label>
                        <input type="password" id="modalConfirmPassword" name="confirm_password" class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-2 focus:ring-indigo-500" autocomplete="new-password">
                    </div>
                </div>"""
new_password = """                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
                        <div class="relative">
                            <input type="password" id="modalPassword" name="password" class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-2 focus:ring-indigo-500 pr-10" autocomplete="new-password">
                            <button type="button" onclick="togglePassword('modalPassword', this)" class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600">
                                <i class="fa-solid fa-eye-slash"></i>
                            </button>
                        </div>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Confirm Password</label>
                        <div class="relative">
                            <input type="password" id="modalConfirmPassword" name="confirm_password" class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-2 focus:ring-indigo-500 pr-10" autocomplete="new-password">
                            <button type="button" onclick="togglePassword('modalConfirmPassword', this)" class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600">
                                <i class="fa-solid fa-eye-slash"></i>
                            </button>
                        </div>
                    </div>
                </div>"""
content = content.replace(old_password, new_password)

with open('templates/website/teachers.html', 'w') as f:
    f.write(content)
