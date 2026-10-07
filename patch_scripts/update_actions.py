with open('templates/website/students.html', 'r') as f:
    content = f.read()

import re

# Swap TH
old_thead = '''                    <th class="py-2.5 px-4 font-semibold w-10 text-center"><input type="checkbox" class="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-offset-0 focus:ring-blue-200 focus:ring-opacity-50"></th>
                    <th class="py-2.5 px-4 font-semibold cursor-pointer hover:bg-gray-100 flex items-center">Student Name <i class="fa-solid fa-sort ml-1 text-gray-400"></i></th>
                    <th class="py-2.5 px-4 font-semibold text-center border-l border-r border-gray-100">Actions</th>
                    <th class="py-2.5 px-4 font-semibold cursor-pointer hover:bg-gray-100">Phone <i class="fa-solid fa-sort ml-1 text-gray-400"></i></th>
                    <th class="py-2.5 px-4 font-semibold cursor-pointer hover:bg-gray-100">Email <i class="fa-solid fa-sort ml-1 text-gray-400"></i></th>
                    <th class="py-2.5 px-4 font-semibold cursor-pointer hover:bg-gray-100">Status <i class="fa-solid fa-sort ml-1 text-gray-400"></i></th>
                    <th class="py-2.5 px-4 font-semibold cursor-pointer hover:bg-gray-100">Created On <i class="fa-solid fa-sort ml-1 text-gray-400"></i></th>'''

new_thead = '''                    <th class="py-2.5 px-4 font-semibold w-10 text-center"><input type="checkbox" class="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-offset-0 focus:ring-blue-200 focus:ring-opacity-50"></th>
                    <th class="py-2.5 px-4 font-semibold cursor-pointer hover:bg-gray-100 flex items-center">Student Name <i class="fa-solid fa-sort ml-1 text-gray-400"></i></th>
                    <th class="py-2.5 px-4 font-semibold cursor-pointer hover:bg-gray-100">Phone <i class="fa-solid fa-sort ml-1 text-gray-400"></i></th>
                    <th class="py-2.5 px-4 font-semibold cursor-pointer hover:bg-gray-100">Email <i class="fa-solid fa-sort ml-1 text-gray-400"></i></th>
                    <th class="py-2.5 px-4 font-semibold cursor-pointer hover:bg-gray-100">Status <i class="fa-solid fa-sort ml-1 text-gray-400"></i></th>
                    <th class="py-2.5 px-4 font-semibold cursor-pointer hover:bg-gray-100">Created On <i class="fa-solid fa-sort ml-1 text-gray-400"></i></th>
                    <th class="py-2.5 px-4 font-semibold text-center border-l border-gray-100">Actions</th>'''

content = content.replace(old_thead, new_thead)

# Swap TD
old_td_regex = r'<td class="py-2.5 px-4 flex items-center space-x-2">.*?<td class="py-2.5 px-4 text-gray-500">{{ student.created_date\|date:"m/d/Y h:i A" }}</td>'

def replace_td(match):
    text = match.group(0)
    
    # Extract the parts
    name_td = re.search(r'<td class="py-2.5 px-4 flex items-center space-x-2">.*?</td>', text, re.DOTALL).group(0)
    
    actions_td_match = re.search(r'<td class="py-2.5 px-4 text-center border-l border-r border-gray-100 text-gray-400 text-lg space-x-3">(.*?)</td>', text, re.DOTALL)
    actions_td_inner = actions_td_match.group(1)
    
    # Remove mail, phone, ellipsis from inner
    actions_td_inner = re.sub(r'<i class="fa-regular fa-envelope.*?</i>', '', actions_td_inner, flags=re.DOTALL)
    actions_td_inner = re.sub(r'<i class="fa-solid fa-phone-flip.*?</i>', '', actions_td_inner, flags=re.DOTALL)
    actions_td_inner = re.sub(r'<i class="fa-solid fa-ellipsis.*?</i>', '', actions_td_inner, flags=re.DOTALL)
    
    new_actions_td = f'<td class="py-2.5 px-4 text-center border-l border-gray-100 text-gray-400 text-lg space-x-3">{actions_td_inner}</td>'
    
    # Remove old actions_td from text
    text_without_actions = text.replace(actions_td_match.group(0), '')
    
    # Now append the new actions_td at the very end
    final_text = text_without_actions + "\n                    " + new_actions_td
    
    return final_text

content = re.sub(old_td_regex, replace_td, content, flags=re.DOTALL)

with open('templates/website/students.html', 'w') as f:
    f.write(content)
