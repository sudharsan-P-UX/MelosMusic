with open('templates/website/courses_batches.html', 'r') as f:
    content = f.read()

bad_head = """                        <th class="py-3 px-6 text-center text-xs font-bold text-gray-700 uppercase tracking-wider">Duration</th>
                        <th class="py-3 px-6 text-right text-xs font-bold text-gray-700 uppercase tracking-wider">Fee (₹)</th>"""
good_head = """                        <th class="py-3 px-6 text-center text-xs font-bold text-gray-700 uppercase tracking-wider">Duration</th>
                        <th class="py-3 px-6 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">Days</th>
                        <th class="py-3 px-6 text-right text-xs font-bold text-gray-700 uppercase tracking-wider">Fee (₹)</th>"""
content = content.replace(bad_head, good_head)

bad_row = """                        <td class="py-3 px-6 text-center text-gray-600">{% if course.duration_months %}{{ course.duration_months }} Months{% else %}-{% endif %}</td>
                        <td class="py-3 px-6 text-right font-bold text-gray-800">{{ course.fee_amount|default:"0.00" }}</td>"""
good_row = """                        <td class="py-3 px-6 text-center text-gray-600">{% if course.duration_months %}{{ course.duration_months }} Months{% else %}-{% endif %}</td>
                        <td class="py-3 px-6 text-gray-600">{{ course.days|default:"-" }}</td>
                        <td class="py-3 px-6 text-right font-bold text-gray-800">{{ course.fee_amount|default:"0.00" }}</td>"""
content = content.replace(bad_row, good_row)

bad_empty = """                    <tr><td colspan="5" class="py-6 text-center text-gray-500">No courses available.</td></tr>"""
good_empty = """                    <tr><td colspan="6" class="py-6 text-center text-gray-500">No courses available.</td></tr>"""
content = content.replace(bad_empty, good_empty)

with open('templates/website/courses_batches.html', 'w') as f:
    f.write(content)
