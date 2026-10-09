import re

with open('mobile_app/lib/screens/dashboard_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace `title: title` and `$title` with `title: name` and `$name` (or wait, the original casing of the menu name is lost because `name = name.toLowerCase()`.
# Wait, I should probably pass a capitalized version of the name or just pass it as is.
# The parameter is `name`.
# In my previous code, the parameter was `name`. But `name` gets lowercase. 
# Let me change the method to accept both or just title-case it.

replacement = """    } else {
      // Capitalize the first letter for the title
      String displayTitle = name.split(' ').map((word) => word.isNotEmpty ? word[0].toUpperCase() + word.substring(1) : '').join(' ');
      Navigator.push(context, MaterialPageRoute(builder: (context) => GenericListScreen(title: displayTitle, endpoint: 'mobile-generic?menu=$name')));
    }"""

text = re.sub(r'\} else \{\s*Navigator\.push.*?GenericListScreen.*?\}\s*\}', replacement + '\n  }', text, flags=re.DOTALL)

with open('mobile_app/lib/screens/dashboard_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)
