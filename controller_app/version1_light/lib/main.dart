import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'fulldpad.dart';
import 'Dpadbutton.dart';

void main() {
  SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersiveSticky);
  SystemChrome.setPreferredOrientations(
      [DeviceOrientation.landscapeLeft, DeviceOrientation.landscapeRight]);
  runApp(const MaterialApp(
    home: Controller(),
  ));
}

class Controller extends StatefulWidget {
  const Controller({super.key});

  @override
  State<Controller> createState() => _ControllerState();
}

class _ControllerState extends State<Controller> {
  double iconSize = 40;
  // String boxText = 'Connection Lost';
  List<String> boxText = [
    'Connection Lost',
    'Welcome Gamer',
    '5-2',
    '5-3',
    'You Won'
  ];
  int boxTextind = 0;
  double containerSize = 250;

  @override
  Widget build(BuildContext context) {
    SystemChrome.setPreferredOrientations([
      DeviceOrientation.landscapeLeft,
      DeviceOrientation.landscapeRight,
    ]);
    SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersiveSticky);
    double screenWidth = MediaQuery.of(context).size.width;
    double screenHeight = MediaQuery.of(context).size.height;
    return Scaffold(
      // backgroundColor: Color.fromARGB(255, 0, 31, 57), //theme
      backgroundColor: Colors.white.withOpacity(0.7),
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: <Widget>[
          Container(
              margin:
                  EdgeInsets.fromLTRB(screenWidth / 4, 10, screenWidth / 4, 10),
              height: 70,
              decoration: BoxDecoration(
                // color: Colors.black, //theme
                color: Colors.black.withOpacity(0.5),
                borderRadius: BorderRadius.all(Radius.circular(35)),
                boxShadow: [
                  // BoxShadow(
                  //   color: Colors.black.withOpacity(0.5), // Outer shadow color
                  //   offset: Offset(-1, 1),
                  //   blurRadius: 4,
                  //   spreadRadius: 2,
                  // ),
                  BoxShadow(
                    color: Colors.white.withOpacity(0.3), // Inner shadow color
                    offset: Offset(1, -1),
                    blurRadius: 5,
                    spreadRadius: -4,
                  ),
                ],
                // border: Border.all(color: Colors.green, width: 2),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  GestureDetector(
                      onTap: () {
                        showDialog(
                          context: context,
                          builder: (BuildContext context) {
                            return AlertDialog(
                              backgroundColor: Colors.black,
                              title: Center(
                                  child: Text(
                                "NETWORK DETAILS",
                                style: TextStyle(color: Colors.green),
                              )),
                              content: Center(
                                  child: Text(
                                      "IPADDRESS : 192.168.200.5\nSERVER STATUS: CONNECTED ",
                                      style: TextStyle(
                                          color: Colors
                                              .white))), // Replace with your string
                              actions: [
                                TextButton(
                                  onPressed: () {
                                    Navigator.of(context).pop();
                                  },
                                  child: Text("Close"),
                                ),
                              ],
                            );
                          },
                        );
                      },
                      child: Icon(
                        Icons.wifi_rounded,
                        color: const Color.fromARGB(255, 0, 255, 8),
                        size: iconSize,
                        shadows: [
                          Shadow(
                              color: Colors.green.withOpacity(0.5),
                              blurRadius: 40)
                        ],
                      )),
                  Container(
                      margin: EdgeInsets.fromLTRB(30, 0, 0, 0),
                      child: Text(
                        '${boxText[boxTextind]}',
                        style: TextStyle(
                            color: const Color.fromARGB(255, 0, 255, 8),
                            fontSize: 35),
                      ))
                ],
              )),
          // Divider(height: 10,),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: <Widget>[
              Transform.translate(
                offset: Offset(-50, 0),
                child: Transform.scale(
                    scale: 1.1, child: FullDpad(containerSize: containerSize)),
              ),
              Transform.translate(
                offset: Offset(50, 40),
                child: Container(
                  width: screenWidth / 3,
                  // color: Colors.red,
                  child: Transform.translate(
                    offset: Offset(0, 0),
                    child: Transform.scale(
                      scale: 1.1,
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.end,
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                            children: [
                              DPadButton(
                                  index: 5,
                                  icon: Icons.block,
                                  onPressed: () {
                                    setState(() {
                                      boxTextind = (boxTextind + 1) % 5;
                                    });
                                  }),
                              DPadButton(
                                  index: 6,
                                  icon: Icons.mic_rounded,
                                  onPressed: () {})
                            ],
                          ),
                          SizedBox(
                            height: 10,
                          ),
                          Transform.translate(
                              offset: Offset(50, 0),
                              child: Row(
                                mainAxisAlignment:
                                    MainAxisAlignment.spaceEvenly,
                                children: [
                                  DPadButton(
                                      index: 7,
                                      icon: Icons.favorite,
                                      onPressed: () {}),
                                  DPadButton(
                                      index: 8,
                                      icon: Icons.electric_bolt,
                                      onPressed: () {})
                                ],
                              )),
                        ],
                      ),
                    ),
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
