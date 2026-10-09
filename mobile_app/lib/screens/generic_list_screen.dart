import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../api_service.dart';

class GenericListScreen extends StatefulWidget {
  final String title;
  final String endpoint;

  GenericListScreen({required this.title, required this.endpoint});

  @override
  _GenericListScreenState createState() => _GenericListScreenState();
}

class _GenericListScreenState extends State<GenericListScreen> {
  List<dynamic> _records = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchData();
  }

  Future<void> _fetchData() async {
    try {
      final response = await http.get(Uri.parse('${ApiService.baseUrl}/${widget.endpoint}/'));
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        if (data['success']) {
          setState(() {
            _records = data['data'];
          });
        }
      }
    } catch (e) {
      print('Error fetching data: $e');
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
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
          : _records.isEmpty
              ? Center(child: Text('No records found.'))
              : ListView.builder(
                  padding: EdgeInsets.all(8.0),
                  itemCount: _records.length,
                  itemBuilder: (context, index) {
                    final record = _records[index];
                    return Card(
                      elevation: 2,
                      margin: EdgeInsets.symmetric(vertical: 6.0, horizontal: 4.0),
                      child: Padding(
                        padding: EdgeInsets.all(16.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: record.entries.map<Widget>((entry) {
                            String key = entry.key.replaceAll('__', ' ').replaceAll('_', ' ').toUpperCase();
                            String value = entry.value?.toString() ?? 'N/A';
                            return Padding(
                              padding: const EdgeInsets.only(bottom: 6.0),
                              child: Row(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Expanded(
                                    flex: 2,
                                    child: Text(
                                      key,
                                      style: TextStyle(fontWeight: FontWeight.bold, color: Colors.grey[700], fontSize: 12),
                                    ),
                                  ),
                                  Expanded(
                                    flex: 3,
                                    child: Text(
                                      value,
                                      style: TextStyle(color: Colors.black87, fontSize: 14),
                                    ),
                                  ),
                                ],
                              ),
                            );
                          }).toList(),
                        ),
                      ),
                    );
                  },
                ),
    );
  }
}
