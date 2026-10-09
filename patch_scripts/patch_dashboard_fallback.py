import re

with open('mobile_app/lib/screens/dashboard_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

fallback_routing = """    } else {
      Navigator.push(context, MaterialPageRoute(builder: (context) => GenericListScreen(title: title, endpoint: 'mobile-generic?menu=$title')));
    }"""

# Replace the ScaffoldMessenger block
import re
text = re.sub(r'\} else \{\s*ScaffoldMessenger.*?\}\s*\}', fallback_routing + '\n  }', text, flags=re.DOTALL)

with open('mobile_app/lib/screens/dashboard_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)
