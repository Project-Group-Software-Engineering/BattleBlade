import 'package:flutter/material.dart';
import 'package:vibration/vibration.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'dart:async';
import 'dart:convert';

class DPadButton extends StatefulWidget {
  final int index;
  final IconData icon;
  int player;
  int control;

  DPadButton({
    Key? key,
    required this.index,
    required this.icon,
    required this.player,
    required this.control,
  }) : super(key: key);

  @override
  State<DPadButton> createState() => _DPadButtonState();
}

class _DPadButtonState extends State<DPadButton> {
  Future<void> _vibrate() async {
    bool? hasVibrator = await Vibration.hasVibrator();
    if (hasVibrator ?? false) {
      Vibration.vibrate(duration: 7);
    }
  }

  //websocketpart//
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
      Uri.parse('ws://10.81.66.51:8765'),
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
      _sendControl(widget.player, widget.control);
    });
  }

  void _stopSending() {
    _reconnectTimer.cancel();
  }

  @override
  Widget build(BuildContext context) {
    return Listener(
      onPointerDown: (details) {
        _vibrate();
        _startSendingRepeatedly(widget.player, widget.control);
      },
      onPointerUp: (details) {
        _vibrate();
        _stopSending();
      },
      onPointerCancel: (details) {
        _stopSending();
      },
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          borderRadius:
              BorderRadius.circular(30), // Adjust border radius as needed
          splashColor: Colors.black.withOpacity(1), // Customize splash color
          onTap: () {
            _vibrate();
            // _startSendingRepeatedly(widget.player, widget.control);
          },
          // onTapCancel: () {
          //   _vibrate();
          //   _stopSending();
          // },
          child: Container(
            width: 60,
            height: 60,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              color: Colors.white.withOpacity(0.7),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.5), // Outer shadow color
                  offset: Offset(-1, 1),
                  blurRadius: 4,
                  spreadRadius: 2,
                ),
                BoxShadow(
                  color: Colors.white.withOpacity(0.3), // Inner shadow color
                  offset: Offset(1, -1),
                  blurRadius: 5,
                  spreadRadius: -4,
                ),
              ],
            ),
            child: Center(
              child: Icon(widget.icon),
            ),
          ),
        ),
      ),
    );
  }
}
