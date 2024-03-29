import 'package:flutter/material.dart';
import 'package:vibration/vibration.dart';


class DPadButton extends StatelessWidget {
  final int index;
  final VoidCallback onPressed;
  final IconData icon;

  Future<void> _vibrate() async {
    bool? hasVibrator = await Vibration.hasVibrator();
    if (hasVibrator ?? false) {
      Vibration.vibrate(duration: 25);
    }
  }

  const DPadButton({
    Key? key,
    required this.index,
    required this.icon,
    required this.onPressed,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: (){
        onPressed();
        _vibrate();
      },
      child: Container(
        width: 60,
        height: 60,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          color: Colors.white.withOpacity(0.7),
          // color: Color.fromARGB(255, 0, 75, 136),
          // color: Colors.grey.withOpacity(0.8),
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
            child: Icon(icon),
        ),
      ),
    );
  }
}
