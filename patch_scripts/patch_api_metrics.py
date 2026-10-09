import re

with open('mobile_app/lib/api_service.dart', 'r', encoding='utf-8') as f:
    text = f.read()

new_method = """
  Future<List<dynamic>> getDashboardMetrics() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/mobile-dashboard-metrics/'));
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['success'] ? data['data'] : [];
      }
    } catch (e) { print(e); }
    return [];
  }
}
"""

text = text.replace("}\n", new_method)
# Wait! I did replace("}\n") previously which ruined the file. Let me do a safer replacement.
# Find the last closing brace and replace it.
text = text.rsplit('}', 1)[0] + new_method

with open('mobile_app/lib/api_service.dart', 'w', encoding='utf-8') as f:
    f.write(text)
