import re

with open('templates/base.html', 'r') as f:
    content = f.read()

# Add ID to nav
old_nav = '<nav class="flex-1 overflow-y-auto py-4 px-3 space-y-1">'
new_nav = '<nav id="sidebar-nav" class="flex-1 overflow-y-auto py-4 px-3 space-y-1">'
if 'id="sidebar-nav"' not in content:
    content = content.replace(old_nav, new_nav)

# Add script block at the end of body
script_block = """
    <!-- Restore Sidebar Scroll Position -->
    <script>
        document.addEventListener("DOMContentLoaded", function() { 
            const sidebar = document.getElementById('sidebar-nav');
            if (sidebar) {
                const scrollpos = sessionStorage.getItem('sidebar-scrollpos');
                if (scrollpos) {
                    sidebar.scrollTop = parseInt(scrollpos, 10);
                }
                
                // Save scroll position before leaving the page
                window.addEventListener('beforeunload', function() {
                    sessionStorage.setItem('sidebar-scrollpos', sidebar.scrollTop);
                });
            }
        });
    </script>
</body>"""

if 'Restore Sidebar Scroll Position' not in content:
    content = content.replace('</body>', script_block)

with open('templates/base.html', 'w') as f:
    f.write(content)
