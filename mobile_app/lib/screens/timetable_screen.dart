import 'package:flutter/material.dart';
import '../api_service.dart';

class TimetableScreen extends StatefulWidget {
  @override
  _TimetableScreenState createState() => _TimetableScreenState();
}

class _TimetableScreenState extends State<TimetableScreen> {
  final ApiService _apiService = ApiService();
  List<dynamic> _timetables = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchData();
  }

  Future<void> _fetchData() async {
    final data = await _apiService.getTimetable();
    setState(() {
      _timetables = data;
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Timetable'),
        backgroundColor: Colors.indigo,
      ),
      body: _isLoading 
          ? Center(child: CircularProgressIndicator())
          : _timetables.isEmpty
              ? Center(child: Text('No timetable found.'))
              : ListView.builder(
                  padding: EdgeInsets.all(8.0),
                  itemCount: _timetables.length,
                  itemBuilder: (context, index) {
                    final schedule = _timetables[index];
                    return Card(
                      elevation: 2,
                      margin: EdgeInsets.symmetric(vertical: 8.0, horizontal: 4.0),
                      child: Padding(
                        padding: EdgeInsets.all(16.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                Text(
                                  schedule['day_of_week'] ?? 'Unknown Day',
                                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.indigo),
                                ),
                                Container(
                                  padding: EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                                  decoration: BoxDecoration(
                                    color: Colors.green[100],
                                    borderRadius: BorderRadius.circular(12),
                                  ),
                                  child: Text(
                                    '${schedule['start_time']} - ${schedule['end_time']}',
                                    style: TextStyle(fontWeight: FontWeight.bold, color: Colors.green[800]),
                                  ),
                                ),
                              ],
                            ),
                            SizedBox(height: 12),
                            Row(
                              children: [
                                Icon(Icons.school, size: 16, color: Colors.grey[600]),
                                SizedBox(width: 8),
                                Text('Course: ${schedule['course__course_name'] ?? 'N/A'}'),
                              ],
                            ),
                            SizedBox(height: 4),
                            Row(
                              children: [
                                Icon(Icons.group, size: 16, color: Colors.grey[600]),
                                SizedBox(width: 8),
                                Text('Batch: ${schedule['batch__batch_name'] ?? 'N/A'}'),
                              ],
                            ),
                            SizedBox(height: 4),
                            Row(
                              children: [
                                Icon(Icons.person, size: 16, color: Colors.grey[600]),
                                SizedBox(width: 8),
                                Text('Teacher: ${schedule['teacher__first_name'] ?? 'N/A'}'),
                              ],
                            ),
                          ],
                        ),
                      ),
                    );
                  },
                ),
    );
  }
}
