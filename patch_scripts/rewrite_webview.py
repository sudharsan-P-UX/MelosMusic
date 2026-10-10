import os
import shutil

# Remove all existing lib files
lib_path = 'mobile_app/lib'
if os.path.exists(lib_path):
    shutil.rmtree(lib_path)
os.makedirs(lib_path)

# Write pubspec.yaml
pubspec = """name: melos_music_mobile
description: Melos Music WebWrapper

publish_to: 'none'

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  webview_flutter: any

dev_dependencies:
  flutter_test:
    sdk: flutter

flutter:
  uses-material-design: true
"""
with open('mobile_app/pubspec.yaml', 'w') as f:
    f.write(pubspec)

# Write main.dart
main_dart = """import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "Melo's Music",
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.indigo,
      ),
      home: const WebViewScreen(),
    );
  }
}

class WebViewScreen extends StatefulWidget {
  const WebViewScreen({Key? key}) : super(key: key);

  @override
  _WebViewScreenState createState() => _WebViewScreenState();
}

class _WebViewScreenState extends State<WebViewScreen> {
  late final WebViewController controller;
  bool isLoading = true;
  String errorMessage = "";

  @override
  void initState() {
    super.initState();
    try {
      controller = WebViewController()
        ..setJavaScriptMode(JavaScriptMode.unrestricted)
        ..setNavigationDelegate(
          NavigationDelegate(
            onPageFinished: (String url) {
              setState(() {
                isLoading = false;
              });
            },
            onWebResourceError: (WebResourceError error) {
              setState(() {
                errorMessage = "Failed to load: ${error.description}";
                isLoading = false;
              });
            },
          ),
        )
        ..loadRequest(Uri.parse('https://melosmusic.vercel.app/login'));
    } catch (e) {
      // Fallback for older webview versions if FlutLab downgrades
      setState(() {
        errorMessage = "FlutLab environment may not support WebViewController. Try building the APK.";
        isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Stack(
          children: [
            if (errorMessage.isEmpty) WebViewWidget(controller: controller),
            if (isLoading)
              const Center(
                child: CircularProgressIndicator(),
              ),
            if (errorMessage.isNotEmpty)
              Center(
                child: Padding(
                  padding: const EdgeInsets.all(20.0),
                  child: Text(
                    errorMessage,
                    style: const TextStyle(color: Colors.red, fontSize: 16),
                    textAlign: TextAlign.center,
                  ),
                ),
              )
          ],
        ),
      ),
    );
  }
}
"""
with open('mobile_app/lib/main.dart', 'w') as f:
    f.write(main_dart)
