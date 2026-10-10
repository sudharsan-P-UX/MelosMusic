import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  static const String baseUrl = 'https://melosmusic.vercel.app/api';

  Future<Map<String, dynamic>> login(String username, String password) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/mobile-login/'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'username': username, 'password': password}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        if (data['success'] == true) {
          final prefs = await SharedPreferences.getInstance();
          await prefs.setInt('user_id', data['user_id']);
          await prefs.setString('role', data['role']);
          await prefs.setString('first_name', data['first_name']);
          return {'success': true, 'role': data['role']};
        } else {
          return {'success': false, 'message': data['error']};
        }
      } else {
        return {'success': false, 'message': 'Server error'};
      }
    } catch (e) {
      return {'success': false, 'message': e.toString()};
    }
  }

  Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.clear();
  }

  Future<bool> isLoggedIn() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.containsKey('user_id');
  }

  Future<List<dynamic>> getStudents() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/mobile-students/'));
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['success'] ? data['data'] : [];
      }
    } catch (e) { print(e); }
    return [];
  }

  Future<List<dynamic>> getTeachers() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/mobile-teachers/'));
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['success'] ? data['data'] : [];
      }
    } catch (e) { print(e); }
    return [];
  }

  Future<List<dynamic>> getCourses() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/mobile-courses/'));
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['success'] ? data['data'] : [];
      }
    } catch (e) { print(e); }
    return [];
  }

  Future<List<dynamic>> getTimetable() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/mobile-timetable/'));
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['success'] ? data['data'] : [];
      }
    } catch (e) { print(e); }
    return [];
  }

  Future<List<dynamic>> getMenus(int userId) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/mobile-menus/'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'user_id': userId}),
      );
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['success'] ? data['data'] : [];
      }
    } catch (e) { print(e); }
    return [];
  }

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
