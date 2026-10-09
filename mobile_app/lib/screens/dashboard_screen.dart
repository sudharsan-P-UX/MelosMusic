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

  Color _getColorForMenu(int index) {
    List<Color> colors = [Colors.blue, Colors.orange, Colors.purple, Colors.green, Colors.teal, Colors.red, Colors.indigo];
    return colors[index % colors.length];
  }

  void _handleMenuTap(String name) {
    name = name.toLowerCase();
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
    } else if (name.contains('user')) {
      Navigator.push(context, MaterialPageRoute(builder: (context) => GenericListScreen(title: 'Users', endpoint: 'mobile-users')));
    } else if (name.contains('role')) {
      Navigator.push(context, MaterialPageRoute(builder: (context) => GenericListScreen(title: 'Roles', endpoint: 'mobile-roles')));
    } else if (name.contains('audit')) {
      Navigator.push(context, MaterialPageRoute(builder: (context) => GenericListScreen(title: 'Audit Logs', endpoint: 'mobile-auditlogs')));
        } else if (name.contains('event')) {
      Navigator.push(context, MaterialPageRoute(builder: (context) => GenericListScreen(title: 'Events', endpoint: 'mobile-events')));
    } else if (name.contains('setting')) {
      Navigator.push(context, MaterialPageRoute(builder: (context) => GenericListScreen(title: 'Settings', endpoint: 'mobile-settings')));
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Screen for "$name" coming soon!')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Dashboard'),
        backgroundColor: Colors.indigo,
        actions: [
          IconButton(
            icon: Icon(Icons.logout),
            onPressed: _logout,
          ),
        ],
      ),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Welcome, $_firstName!',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 8),
            Text(
              'Role: $_role',
              style: TextStyle(fontSize: 16, color: Colors.grey[700]),
            ),
            SizedBox(height: 32),
            Expanded(
              child: _isLoading 
                  ? Center(child: CircularProgressIndicator())
                  : GridView.builder(
                      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                        crossAxisCount: 2,
                        crossAxisSpacing: 16,
                        mainAxisSpacing: 16,
                      ),
                      itemCount: _menus.length,
                      itemBuilder: (context, index) {
                        final menu = _menus[index];
                        final menuName = menu['menu_name'];
                        return _buildDashboardCard(
                          menuName, 
                          _getIconForMenu(menuName), 
                          _getColorForMenu(index)
                        );
                      },
                    ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDashboardCard(String title, IconData icon, Color color) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: InkWell(
        onTap: () => _handleMenuTap(title),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 48, color: color),
            SizedBox(height: 16),
            Text(title, textAlign: TextAlign.center, style: TextStyle(fontSize: 14, fontWeight: FontWeight.w500)),
          ],
        ),
      ),
    );
  }
}
