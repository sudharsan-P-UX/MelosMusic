import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../api_service.dart';
import 'login_screen.dart';
import 'user_list_screen.dart';
import 'course_list_screen.dart';
import 'timetable_screen.dart';
import 'generic_list_screen.dart';

class DashboardScreen extends StatefulWidget {
  @override
  _DashboardScreenState createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  String _firstName = '';
  String _role = '';
  int _userId = 0;
  List<dynamic> _menus = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadUserData();
  }

  Future<void> _loadUserData() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      _firstName = prefs.getString('first_name') ?? 'User';
      _role = prefs.getString('role') ?? 'Student';
      _userId = prefs.getInt('user_id') ?? 0;
    });
    _fetchMenus();
  }

  Future<void> _fetchMenus() async {
    if (_userId != 0) {
      final menus = await ApiService().getMenus(_userId);
      setState(() {
        _menus = menus;
        _isLoading = false;
      });
    }
  }

  Future<void> _logout() async {
    await ApiService().logout();
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(builder: (context) => LoginScreen()),
    );
  }

  IconData _getIconForMenu(String name) {
    name = name.toLowerCase();
    if (name.contains('student')) return Icons.people;
    if (name.contains('teacher')) return Icons.school;
    if (name.contains('course')) return Icons.music_video;
    if (name.contains('time')) return Icons.schedule;
    if (name.contains('fee')) return Icons.attach_money;
    if (name.contains('attend')) return Icons.calendar_today;
    if (name.contains('event')) return Icons.event;
    if (name.contains('user') || name.contains('role')) return Icons.manage_accounts;
    if (name.contains('setting')) return Icons.settings;
    if (name.contains('audit')) return Icons.security;
    return Icons.folder;
  }

  void _handleMenuTap(String name) {
    name = name.toLowerCase();
    if (name.contains('dashboard')) {
      return; // Already on dashboard
    }
    if (name.contains('student') && !name.contains('attendance')) {
      Navigator.push(context, MaterialPageRoute(builder: (context) => UserListScreen(title: 'Students', type: 'student')));
    } else if (name.contains('teacher') && !name.contains('attendance')) {
      Navigator.push(context, MaterialPageRoute(builder: (context) => UserListScreen(title: 'Teachers', type: 'teacher')));
    } else if (name.contains('course') && !name.contains('allocation')) {
      Navigator.push(context, MaterialPageRoute(builder: (context) => CourseListScreen()));
    } else if (name.contains('time')) {
      Navigator.push(context, MaterialPageRoute(builder: (context) => TimetableScreen()));
    } else if (name.contains('attend')) {
      Navigator.push(context, MaterialPageRoute(builder: (context) => GenericListScreen(title: 'Attendance', endpoint: 'mobile-attendance')));
    } else if (name.contains('fee')) {
      Navigator.push(context, MaterialPageRoute(builder: (context) => GenericListScreen(title: 'Fees', endpoint: 'mobile-fees')));
    } else if (name.contains('event')) {
      Navigator.push(context, MaterialPageRoute(builder: (context) => GenericListScreen(title: 'Events', endpoint: 'mobile-events')));
    } else if (name.contains('user')) {
      Navigator.push(context, MaterialPageRoute(builder: (context) => GenericListScreen(title: 'Users', endpoint: 'mobile-users')));
    } else if (name.contains('role')) {
      Navigator.push(context, MaterialPageRoute(builder: (context) => GenericListScreen(title: 'Roles', endpoint: 'mobile-roles')));
    } else if (name.contains('setting')) {
      Navigator.push(context, MaterialPageRoute(builder: (context) => GenericListScreen(title: 'Settings', endpoint: 'mobile-settings')));
    } else if (name.contains('audit')) {
      Navigator.push(context, MaterialPageRoute(builder: (context) => GenericListScreen(title: 'Audit Logs', endpoint: 'mobile-auditlogs')));
            } else {
      // Capitalize the first letter for the title
      String displayTitle = name.split(' ').map((word) => word.isNotEmpty ? word[0].toUpperCase() + word.substring(1) : '').join(' ');
      Navigator.push(context, MaterialPageRoute(builder: (context) => GenericListScreen(title: displayTitle, endpoint: 'mobile-generic?menu=$name')));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Melo's Music"),
        backgroundColor: Colors.indigo,
        // The Drawer hamburger icon is automatically added if we provide a drawer
      ),
      drawer: Drawer(
        child: Column(
          children: [
            DrawerHeader(
              decoration: BoxDecoration(color: Colors.indigo),
              margin: EdgeInsets.zero,
              child: Container(
                width: double.infinity,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisAlignment: MainAxisAlignment.end,
                  children: [
                    CircleAvatar(
                      radius: 30,
                      backgroundColor: Colors.white,
                      child: Icon(Icons.person, size: 40, color: Colors.indigo),
                    ),
                    SizedBox(height: 12),
                    Text(
                      _firstName,
                      style: TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold),
                    ),
                    Text(
                      _role,
                      style: TextStyle(color: Colors.indigo[100], fontSize: 14),
                    ),
                  ],
                ),
              ),
            ),
            Expanded(
              child: _isLoading
                  ? Center(child: CircularProgressIndicator())
                  : ListView.builder(
                      padding: EdgeInsets.zero,
                      itemCount: _menus.length,
                      itemBuilder: (context, index) {
                        final menuName = _menus[index]['menu_name'];
                        return ListTile(
                          leading: Icon(_getIconForMenu(menuName), color: Colors.indigo[400]),
                          title: Text(menuName, style: TextStyle(fontSize: 15)),
                          onTap: () {
                            Navigator.pop(context); // Close the drawer
                            _handleMenuTap(menuName);
                          },
                        );
                      },
                    ),
            ),
            Divider(height: 1),
            ListTile(
              leading: Icon(Icons.logout, color: Colors.red[400]),
              title: Text('Logout', style: TextStyle(color: Colors.red[700])),
              onTap: _logout,
            ),
            SizedBox(height: 16),
          ],
        ),
      ),
      body: Center(
        child: Padding(
          padding: EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.dashboard, size: 100, color: Colors.indigo[100]),
              SizedBox(height: 24),
              Text(
                'Welcome to your Dashboard!',
                style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.indigo[900]),
                textAlign: TextAlign.center,
              ),
              SizedBox(height: 16),
              Text(
                'Tap the menu icon (三) in the top left corner to navigate to your accessible modules.',
                style: TextStyle(fontSize: 16, color: Colors.grey[700]),
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
