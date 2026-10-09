import re

with open('mobile_app/lib/api_service.dart', 'r', encoding='utf-8') as f:
    text = f.read()

new_methods = """
  Future<List<dynamic>> getCourses() async {
    final response = await http.get(Uri.parse('$baseUrl/mobile-courses/'));
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return data['success'] ? data['data'] : [];
    }
    return [];
  }

  Future<List<dynamic>> getTimetable() async {
    final response = await http.get(Uri.parse('$baseUrl/mobile-timetable/'));
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return data['success'] ? data['data'] : [];
    }
    return [];
  }
}
"""

text = text.replace("}\n", new_methods)

with open('mobile_app/lib/api_service.dart', 'w', encoding='utf-8') as f:
    f.write(text)
