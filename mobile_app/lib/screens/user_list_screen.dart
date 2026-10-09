import 'package:flutter/material.dart';
import '../api_service.dart';

class UserListScreen extends StatefulWidget {
  final String title;
  final String type; // 'student' or 'teacher'

  UserListScreen({required this.title, required this.type});

  @override
  _UserListScreenState createState() => _UserListScreenState();
}

class _UserListScreenState extends State<UserListScreen> {
  final ApiService _apiService = ApiService();
  List<dynamic> _users = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchData();
  }

  Future<void> _fetchData() async {
    final data = widget.type == 'student' 
        ? await _apiService.getStudents() 
        : await _apiService.getTeachers();
        
    setState(() {
      _users = data;
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
        backgroundColor: Colors.indigo,
      ),
      body: _isLoading 
          ? Center(child: CircularProgressIndicator())
          : _users.isEmpty
              ? Center(child: Text('No ${widget.title.toLowerCase()} found.'))
              : ListView.builder(
                  padding: EdgeInsets.all(8.0),
                  itemCount: _users.length,
                  itemBuilder: (context, index) {
                    final user = _users[index];
                    return Card(
                      child: ListTile(
                        leading: CircleAvatar(
                          backgroundColor: Colors.indigo[100],
                          child: Icon(Icons.person, color: Colors.indigo),
                        ),
                        title: Text(user['first_name'] ?? 'Unknown'),
                        subtitle: Text(user['email'] ?? 'No email'),
                        trailing: IconButton(
                          icon: Icon(Icons.phone, color: Colors.green),
                          onPressed: () {
                            // Dial logic could go here
                          },
                        ),
                      ),
                    );
                  },
                ),
    );
  }
}
