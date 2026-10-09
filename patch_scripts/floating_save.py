import re

with open('templates/website/admin_dashboard.html', 'r') as f:
    content = f.read()

# Replace the Order List cell to just an input with a class
old_order_td = """<td class="py-1.5 px-4 text-center">
                            <form method="POST" action="" class="inline-flex">
                                {% csrf_token %}
                                <input type="hidden" name="action" value="save_menu">
                                <input type="hidden" name="menu_id" value="{{ m.menu_id }}">
                                <input type="hidden" name="menu_name" value="{{ m.menu_name }}">
                                <input type="hidden" name="url_page" value="{{ m.url_page }}">
                                <input type="hidden" name="is_active" value="{% if m.is_active %}on{% endif %}">
                                <input type="number" name="display_order" value="{{ m.display_order }}" class="w-16 border border-gray-300 rounded px-1.5 py-1 text-xs text-center focus:ring-indigo-500 focus:border-indigo-500" onchange="this.form.submit()">
                            </form>
                        </td>"""

new_order_td = """<td class="py-1.5 px-4 text-center">
                            <input type="number" name="order_{{ m.menu_id }}" value="{{ m.display_order }}" class="menu-order-input w-16 border border-gray-300 rounded px-1.5 py-1 text-xs text-center focus:ring-indigo-500 focus:border-indigo-500">
                        </td>"""

content = content.replace(old_order_td, new_order_td)

# Add the frozen save button and form at the end of the menu tab
save_button_html = """
        <!-- Sticky Save Button for Menu Orders -->
        <div x-show="tab === 'menu'" class="fixed bottom-8 right-8 z-40">
            <form id="menuOrderForm" method="POST" action="">
                {% csrf_token %}
                <input type="hidden" name="action" value="save_menu_orders">
                <button type="button" onclick="submitMenuOrders()" class="bg-[#4f46e5] hover:bg-indigo-700 text-white font-medium py-3 px-6 rounded-full shadow-xl flex items-center transition-transform hover:scale-105 border-2 border-white">
                    <i class="fa-solid fa-floppy-disk mr-2"></i> Save Order
                </button>
            </form>
        </div>
        
        <script>
        function submitMenuOrders() {
            const form = document.getElementById('menuOrderForm');
            // Clear previous hidden inputs if clicked multiple times
            form.querySelectorAll('.dynamic-order-input').forEach(e => e.remove());
            
            document.querySelectorAll('.menu-order-input').forEach(input => {
                const hidden = document.createElement('input');
                hidden.type = 'hidden';
                hidden.className = 'dynamic-order-input';
                hidden.name = input.name;
                hidden.value = input.value;
                form.appendChild(hidden);
            });
            form.submit();
        }
        </script>
    </div>
    
    <!-- System Settings Tab -->"""

content = content.replace('    </div>\n    \n    <!-- System Settings Tab -->', save_button_html)

with open('templates/website/admin_dashboard.html', 'w') as f:
    f.write(content)
