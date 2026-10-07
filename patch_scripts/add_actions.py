with open('templates/website/courses_batches.html', 'r') as f:
    content = f.read()

# Course table header
bad_course_th = '<th class="py-3 px-6 text-center text-xs font-bold text-gray-700 uppercase tracking-wider">Status</th>'
good_course_th = '<th class="py-3 px-6 text-center text-xs font-bold text-gray-700 uppercase tracking-wider">Status</th>\n                        <th class="py-3 px-6 text-center text-xs font-bold text-gray-700 uppercase tracking-wider">Action</th>'
content = content.replace(bad_course_th, good_course_th)

# Course table row
bad_course_td = """                        <td class="py-3 px-6 text-center">
                            {% if course.is_active %}
                            <span class="px-2 py-1 bg-green-100 text-green-700 text-xs font-bold rounded">Active</span>
                            {% else %}
                            <span class="px-2 py-1 bg-red-100 text-red-700 text-xs font-bold rounded">Inactive</span>
                            {% endif %}
                        </td>"""
good_course_td = """                        <td class="py-3 px-6 text-center">
                            {% if course.is_active %}
                            <span class="px-2 py-1 bg-green-100 text-green-700 text-xs font-bold rounded">Active</span>
                            {% else %}
                            <span class="px-2 py-1 bg-red-100 text-red-700 text-xs font-bold rounded">Inactive</span>
                            {% endif %}
                        </td>
                        <td class="py-3 px-6 text-center whitespace-nowrap">
                            <a href="#" class="text-blue-500 hover:text-blue-700 mx-1" title="View"><i class="fa-solid fa-eye"></i></a>
                            <a href="#" class="text-indigo-500 hover:text-indigo-700 mx-1" title="Edit"><i class="fa-solid fa-pen-to-square"></i></a>
                            <a href="#" class="text-red-500 hover:text-red-700 mx-1" title="Delete" onclick="return confirm('Are you sure you want to delete this course?');"><i class="fa-solid fa-trash"></i></a>
                        </td>"""
content = content.replace(bad_course_td, good_course_td)

# Batch table header
bad_batch_th = '<th class="py-3 px-4 text-center text-xs font-bold text-gray-700 uppercase tracking-wider">Status</th>'
good_batch_th = '<th class="py-3 px-4 text-center text-xs font-bold text-gray-700 uppercase tracking-wider">Status</th>\n                        <th class="py-3 px-4 text-center text-xs font-bold text-gray-700 uppercase tracking-wider">Action</th>'
content = content.replace(bad_batch_th, good_batch_th)

# Batch table row
bad_batch_td = """                        <td class="py-3 px-4 text-center">
                            {% if batch.is_active %}
                            <span class="px-2 py-1 bg-green-100 text-green-700 text-xs font-bold rounded">Active</span>
                            {% else %}
                            <span class="px-2 py-1 bg-red-100 text-red-700 text-xs font-bold rounded">Inactive</span>
                            {% endif %}
                        </td>"""
good_batch_td = """                        <td class="py-3 px-4 text-center">
                            {% if batch.is_active %}
                            <span class="px-2 py-1 bg-green-100 text-green-700 text-xs font-bold rounded">Active</span>
                            {% else %}
                            <span class="px-2 py-1 bg-red-100 text-red-700 text-xs font-bold rounded">Inactive</span>
                            {% endif %}
                        </td>
                        <td class="py-3 px-4 text-center whitespace-nowrap">
                            <a href="#" class="text-blue-500 hover:text-blue-700 mx-1" title="View"><i class="fa-solid fa-eye"></i></a>
                            <a href="#" class="text-indigo-500 hover:text-indigo-700 mx-1" title="Edit"><i class="fa-solid fa-pen-to-square"></i></a>
                            <a href="#" class="text-red-500 hover:text-red-700 mx-1" title="Delete" onclick="return confirm('Are you sure you want to delete this batch?');"><i class="fa-solid fa-trash"></i></a>
                        </td>"""
content = content.replace(bad_batch_td, good_batch_td)

# Empty colspans
content = content.replace('colspan="6"', 'colspan="7"')

with open('templates/website/courses_batches.html', 'w') as f:
    f.write(content)
