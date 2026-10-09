import re

with open('mobile_app/lib/screens/dashboard_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

new_routing = """    } else if (name.contains('event')) {
      Navigator.push(context, MaterialPageRoute(builder: (context) => GenericListScreen(title: 'Events', endpoint: 'mobile-events')));
    } else if (name.contains('setting')) {
      Navigator.push(context, MaterialPageRoute(builder: (context) => GenericListScreen(title: 'Settings', endpoint: 'mobile-settings')));
    } else {"""

text = text.replace("} else {", new_routing)

with open('mobile_app/lib/screens/dashboard_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)
