import re

with open('templates/base.html', 'r') as f:
    content = f.read()

toast_markup = """
    <!-- Toast Notifications -->
    <div class="fixed top-4 right-4 z-50 flex flex-col space-y-2 pointer-events-none">
        {% if messages %}
            {% for message in messages %}
                <div x-data="{ show: true }" 
                     x-show="show" 
                     x-init="setTimeout(() => show = false, 4000)"
                     x-transition:enter="transition ease-out duration-300 transform"
                     x-transition:enter-start="translate-x-full opacity-0"
                     x-transition:enter-end="translate-x-0 opacity-100"
                     x-transition:leave="transition ease-in duration-200"
                     x-transition:leave-start="opacity-100"
                     x-transition:leave-end="opacity-0 translate-x-full"
                     class="pointer-events-auto flex items-center p-4 rounded shadow-lg max-w-sm w-full 
                     {% if message.tags == 'success' %}bg-green-50 border-l-4 border-green-500 text-green-800
                     {% elif message.tags == 'error' %}bg-red-50 border-l-4 border-red-500 text-red-800
                     {% else %}bg-blue-50 border-l-4 border-blue-500 text-blue-800{% endif %}"
                     role="alert">
                    <div class="mr-3">
                        {% if message.tags == 'success' %}
                            <i class="fa-solid fa-circle-check text-green-500 text-xl"></i>
                        {% elif message.tags == 'error' %}
                            <i class="fa-solid fa-circle-exclamation text-red-500 text-xl"></i>
                        {% else %}
                            <i class="fa-solid fa-circle-info text-blue-500 text-xl"></i>
                        {% endif %}
                    </div>
                    <div class="flex-1 text-sm font-medium">{{ message }}</div>
                    <button @click="show = false" class="ml-4 text-gray-400 hover:text-gray-600 focus:outline-none">
                        <i class="fa-solid fa-xmark"></i>
                    </button>
                </div>
            {% endfor %}
        {% endif %}
    </div>
"""

if '<!-- Toast Notifications -->' not in content:
    # Insert right after <main>
    content = content.replace('<main class="flex-1 flex flex-col relative overflow-y-auto">', '<main class="flex-1 flex flex-col relative overflow-y-auto">' + toast_markup)

with open('templates/base.html', 'w') as f:
    f.write(content)
