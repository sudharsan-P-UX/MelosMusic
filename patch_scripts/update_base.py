with open('templates/base.html', 'r') as f:
    content = f.read()

toast_html = """
    <!-- Toast Messages -->
    <div id="toast-container" class="fixed top-5 right-5 z-[100] flex flex-col gap-3 pointer-events-none">
        {% if messages %}
            {% for message in messages %}
                <div class="toast-message transform transition-all duration-300 translate-x-full opacity-0 max-w-sm w-full bg-white shadow-lg rounded-lg pointer-events-auto overflow-hidden ring-1 ring-black ring-opacity-5">
                    <div class="p-4 flex items-start">
                        <div class="flex-shrink-0">
                            {% if message.tags == 'success' %}
                                <i class="fa-solid fa-circle-check text-green-500 text-xl"></i>
                            {% elif message.tags == 'error' %}
                                <i class="fa-solid fa-circle-xmark text-red-500 text-xl"></i>
                            {% elif message.tags == 'warning' %}
                                <i class="fa-solid fa-triangle-exclamation text-yellow-500 text-xl"></i>
                            {% else %}
                                <i class="fa-solid fa-circle-info text-blue-500 text-xl"></i>
                            {% endif %}
                        </div>
                        <div class="ml-3 w-0 flex-1 pt-0.5">
                            <p class="text-sm font-medium text-gray-900">{{ message }}</p>
                        </div>
                        <div class="ml-4 flex-shrink-0 flex">
                            <button type="button" class="bg-white rounded-md inline-flex text-gray-400 hover:text-gray-500 focus:outline-none" onclick="this.closest('.toast-message').remove()">
                                <span class="sr-only">Close</span>
                                <i class="fa-solid fa-xmark"></i>
                            </button>
                        </div>
                    </div>
                </div>
            {% endfor %}
        {% endif %}
    </div>

    <script>
        // Animate toasts in
        document.addEventListener('DOMContentLoaded', () => {
            const toasts = document.querySelectorAll('.toast-message');
            toasts.forEach((toast, index) => {
                setTimeout(() => {
                    toast.classList.remove('translate-x-full', 'opacity-0');
                }, 100 * index);
                
                // Auto remove after 4 seconds
                setTimeout(() => {
                    toast.classList.add('opacity-0');
                    setTimeout(() => toast.remove(), 300);
                }, 4000 + (100 * index));
            });
        });
    </script>
"""

content = content.replace('</body>', toast_html + '\n</body>')

with open('templates/base.html', 'w') as f:
    f.write(content)
