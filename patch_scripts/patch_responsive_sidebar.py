import re

with open('templates/base.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Add Alpine state to body
text = text.replace(
    '<body class="bg-gray-50 flex h-screen overflow-hidden">',
    '<body class="bg-gray-50 flex h-screen overflow-hidden" x-data="{ sidebarOpen: false }">'
)

# Add backdrop and responsive classes to aside
aside_replacement = """    <!-- Mobile sidebar backdrop -->
    <div x-show="sidebarOpen" x-transition.opacity class="fixed inset-0 z-40 bg-gray-900 bg-opacity-50 md:hidden" @click="sidebarOpen = false"></div>
    
    <!-- Sidebar Menu -->
    <aside :class="{'translate-x-0': sidebarOpen, '-translate-x-full': !sidebarOpen}" class="fixed inset-y-0 left-0 z-50 w-64 bg-indigo-900 text-white flex flex-col transition-transform duration-300 ease-in-out md:relative md:translate-x-0">
        <div class="h-16 flex items-center justify-between px-4 font-bold text-2xl border-b border-indigo-800">
            <span class="mx-auto">Melo's Music</span>
            <button @click="sidebarOpen = false" class="md:hidden text-indigo-300 hover:text-white">
                <i class="fa-solid fa-xmark"></i>
            </button>
        </div>"""

text = re.sub(
    r'<!-- Sidebar Menu -->\s*<aside class="w-64 bg-indigo-900 text-white flex flex-col">\s*<div class="h-16 flex items-center justify-center font-bold text-2xl border-b border-indigo-800">\s*Melo\'s Music\s*</div>',
    aside_replacement,
    text
)

# Add mobile menu toggle to header
header_replacement = """        <header class="h-16 bg-white shadow flex items-center justify-between px-4 md:px-6">
            <div class="flex items-center gap-3">
                <button @click="sidebarOpen = true" class="md:hidden text-gray-500 hover:text-indigo-600 focus:outline-none">
                    <i class="fa-solid fa-bars text-xl"></i>
                </button>
                <h1 class="text-xl font-semibold text-gray-800 truncate max-w-[200px] md:max-w-none">{% block header %}Dashboard{% endblock %}</h1>
            </div>"""

text = re.sub(
    r'<header class="h-16 bg-white shadow flex items-center justify-between px-6">\s*<h1 class="text-xl font-semibold text-gray-800">{% block header %}Dashboard{% endblock %}</h1>',
    header_replacement,
    text
)

# Add @click="sidebarOpen = false" to all anchor tags inside the nav
text = text.replace(
    'class="block px-4 py-1.5',
    '@click="sidebarOpen = false" class="block px-4 py-1.5'
)
text = text.replace(
    'class="block pl-3 py-1.5',
    '@click="sidebarOpen = false" class="block pl-3 py-1.5'
)
text = text.replace(
    'class="block px-4 py-2',
    '@click="sidebarOpen = false" class="block px-4 py-2'
)

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(text)
