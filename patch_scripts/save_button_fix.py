import re

with open('templates/website/admin_dashboard.html', 'r') as f:
    content = f.read()

# Rename the button from "Save Order" to "Save"
old_button = """<i class="fa-solid fa-floppy-disk mr-2"></i> Save Order"""
new_button = """<i class="fa-solid fa-floppy-disk mr-2"></i> Save"""
content = content.replace(old_button, new_button)

# Add an empty row for save
old_table_end = """                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>"""
new_table_end = """                    {% endfor %}
                    <!-- Empty row so the floating save button doesn't overlap the last item -->
                    <tr class="h-20 bg-transparent border-t-0">
                        <td colspan="5"></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>"""

content = content.replace(old_table_end, new_table_end)

with open('templates/website/admin_dashboard.html', 'w') as f:
    f.write(content)
