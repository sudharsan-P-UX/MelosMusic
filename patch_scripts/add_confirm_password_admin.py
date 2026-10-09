import re

with open('templates/website/admin_dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

pattern = r"""(<div>\n\s+<label class="block text-sm font-medium text-gray-700 mb-1">Password</label>\n\s+<input type="password" name="password" autocomplete="new-password" required class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-indigo-500 text-sm">\n\s+</div>)"""

repl = r"""\1
                              <div>
                                  <label class="block text-sm font-medium text-gray-700 mb-1">Confirm Password</label>
                                  <input type="password" name="confirm_password" autocomplete="new-password" required class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-indigo-500 text-sm">
                              </div>"""

text = re.sub(pattern, repl, text)

with open('templates/website/admin_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(text)
