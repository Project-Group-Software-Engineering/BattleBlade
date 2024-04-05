import 'dart:async';
import 'package:flutter/material.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'dart:convert';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    const title = 'WebSocket Controls';
    return MaterialApp(
      title: title,
      home: MyHomePage(
        title: title,
      ),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({Key? key, required this.title}) : super(key: key);

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  late Timer _reconnectTimer;
  late WebSocketChannel _channel;

  @override
  void initState() {
    super.initState();
    _connectWebSocket();
    _startReconnectTimer();
  }

  void _connectWebSocket() {
    _channel = WebSocketChannel.connect(
      Uri.parse('ws://10.81.70.103:8765'),
    );
  }

  void _startReconnectTimer() {
    _reconnectTimer = Timer.periodic(Duration(seconds: 30), (_) {
      _channel.sink.close();
      _connectWebSocket();
    });
  }

  void _sendControl(int player, int control) {
    final message = jsonEncode({
      'player': player,
      'control': control,
    });
    _channel.sink.add(message);
  }

  void _startSendingRepeatedly(int player, int control) {
    // Adjust your sending interval as needed
    _reconnectTimer = Timer.periodic(const Duration(milliseconds: 10), (_) {
      _sendControl(player, control);
    });
  }

  void _stopSending() {
    _reconnectTimer.cancel();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            _controlButton("Left", 1, 1),
            _controlButton("Right", 1, 2),
            _controlButton("Jump", 1, 3),
            _controlButton("Attack 1", 1, 4),
            _controlButton("Attack 2", 1, 5),
          ],
        ),
      ),
    );
  }

  Widget _controlButton(String label, int player, int control) {
    return Listener(
      onPointerDown: (details) {
        _startSendingRepeatedly(player, control);
      },
      onPointerUp: (details) {
        _stopSending();
      },
      onPointerCancel: (details) {
        _stopSending();
      },
      child: Container(
        decoration: BoxDecoration(color: Colors.orange, border: Border.all()),
        padding: const EdgeInsets.all(16.0),
        child: Text(label),
      ),
    );
  }

  @override
  void dispose() {
    _reconnectTimer.cancel();
    _channel.sink.close();
    super.dispose();
  }
}
