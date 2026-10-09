import re

with open('mobile_app/lib/screens/dashboard_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Add a check for 'dashboard' to prevent opening a GenericListScreen
replacement = """  void _handleMenuTap(String name) {
    name = name.toLowerCase();
    if (name.contains('dashboard')) {
      return; // Already on dashboard
    }"""

text = text.replace("  void _handleMenuTap(String name) {\n    name = name.toLowerCase();", replacement)

with open('mobile_app/lib/screens/dashboard_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)
