import 'package:flutter/material.dart';
// ignore: avoid_web_libraries_in_flutter
import 'dart:html' as html;
import 'dart:ui_web' as ui_web;

void main() {
  // Register the iframe for the FlutLab web emulator
  ui_web.platformViewRegistry.registerViewFactory(
    'iframeElement',
    (int viewId) => html.IFrameElement()
      ..src = 'https://melosmusic.vercel.app'
      ..style.border = 'none'
      ..style.width = '100%'
      ..style.height = '100%',
  );

  runApp(const MyApp());
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

class WebViewScreen extends StatelessWidget {
  const WebViewScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: SafeArea(
        child: HtmlElementView(viewType: 'iframeElement'),
      ),
    );
  }
}
