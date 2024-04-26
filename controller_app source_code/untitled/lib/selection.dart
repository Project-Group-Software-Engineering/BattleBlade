import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'fulldpad1.dart';
import 'Dpadbuttonwithoutlistener1.dart';







bool selectflag=false;
class Selector extends StatefulWidget {
  const Selector({super.key});

  @override
  State<Selector> createState() => _SelectorState();
}

class _SelectorState extends State<Selector> {
  double iconSize = 40;
  // String boxText = 'Connection Lost';
  List<String> boxText = [
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
      body: DecoratedBox(
        decoration: BoxDecoration(
          image: DecorationImage(
            image: AssetImage(
                        'C:\\Users\\dell\\StudioProjects\\untitled\\build\\flutter_assets\\bg.jpg'),
            fit: BoxFit.cover,
          )
        ),
        child: Column(
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
                  offset: selectflag?Offset(-50,0):Offset(-20, 0), //change
                  child: Transform.scale(
                      scale: 1.1, child: FullDpad(containerSize: containerSize)),
                ),
        
            DPadButton(
              index: 15, 
              size: 60,
              imagePath:'C:\\Users\\dell\\StudioProjects\\untitled\\build\\flutter_assets\\select_icon.png', 
              player: 1, 
              control: 10, 
              ),
            // Visibility(
            //   visible: !selectflag,
            //   child: ElevatedButton(
            //     style: ElevatedButton.styleFrom(
            //       foregroundColor: Colors.black,
            //       backgroundColor: Colors.red.withOpacity(0.7),
            //       shape: RoundedRectangleBorder(
            //         borderRadius: BorderRadius.circular(30.0),
            //       ),
            //       elevation: 0,
            //     ),
            //     child: Text("Select"),
            //     onPressed: (){
                  
            //       Navigator.pushNamed(context, '/route4');
            //     },
            //   ),
            // ),
        
                Transform.translate(
                  offset: selectflag?Offset(50,40):Offset(15, 40),
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
                            // DPadButton(
                            //             index: 7,
                            //             icon: Icons.favorite,
                            //             // onPressed: () {}
                            //             player: 1,
                            //             control: 10),
                            
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
      ),
    );
  }
}