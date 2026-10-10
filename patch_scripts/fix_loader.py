import re

with open('mobile_app/lib/screens/dashboard_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

replacement = """
            _metrics.isEmpty && _isLoading
                ? Center(child: Padding(padding: EdgeInsets.all(32), child: CircularProgressIndicator()))
                : _metrics.isEmpty 
                    ? Center(child: Text("Could not load metrics. Ensure backend is running.", style: TextStyle(color: Colors.red)))
                    : GridView.builder(
"""

text = text.replace("""
            _metrics.isEmpty
                ? Center(child: Padding(padding: EdgeInsets.all(32), child: CircularProgressIndicator()))
                : GridView.builder(""", replacement)

with open('mobile_app/lib/screens/dashboard_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)
