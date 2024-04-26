import 'package:flutter/material.dart';
import 'welcome(modified).dart';
import 'ipaddress(modified).dart';
import 'controller1.dart';
import 'selection.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Navigation Example',
      initialRoute: '/home',
      routes: {
        '/home': (context) => homepage(),
        '/route1': (context) => homepage(),
        '/route2': (context) => ippage(),
        '/route3': (context) => Selector(),
        '/route4': (context) => Controller(),
      },
    );
  }
}