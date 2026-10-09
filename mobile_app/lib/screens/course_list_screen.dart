import 'package:flutter/material.dart';
import '../api_service.dart';

class CourseListScreen extends StatefulWidget {
  @override
  _CourseListScreenState createState() => _CourseListScreenState();
}

class _CourseListScreenState extends State<CourseListScreen> {
  final ApiService _apiService = ApiService();
  List<dynamic> _courses = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchData();
  }

  Future<void> _fetchData() async {
    final data = await _apiService.getCourses();
    setState(() {
      _courses = data;
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Courses'),
        backgroundColor: Colors.indigo,
      ),
      body: _isLoading 
          ? Center(child: CircularProgressIndicator())
          : _courses.isEmpty
              ? Center(child: Text('No courses found.'))
              : ListView.builder(
                  padding: EdgeInsets.all(8.0),
                  itemCount: _courses.length,
                  itemBuilder: (context, index) {
                    final course = _courses[index];
                    return Card(
                      child: ListTile(
                        leading: Icon(Icons.music_video, color: Colors.indigo),
                        title: Text(course['course_name'] ?? 'Unknown Course'),
                        subtitle: Text(course['description'] ?? ''),
                      ),
                    );
                  },
                ),
    );
  }
}
