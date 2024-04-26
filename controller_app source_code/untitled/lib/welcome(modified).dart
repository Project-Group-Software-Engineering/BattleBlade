import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:gradient_borders/box_borders/gradient_box_border.dart';





class homepage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    
    double deviceWidth = MediaQuery.of(context).size.width;

    return Scaffold(
      backgroundColor: Color.fromARGB(255, 75, 62, 80),
      body: Container(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Align(
              alignment: Alignment.centerRight,
              child: Container(
                height: deviceWidth *
                    0.9, 
                width: deviceWidth * 1.0,
                decoration: BoxDecoration(
                  image: DecorationImage(
                    image: AssetImage(
                        'C:\\Users\\dell\\StudioProjects\\untitled\\build\\flutter_assets\\top.png'), 
                    fit: BoxFit.fill,
                  ),
                ),
              ),
            ),
            Container(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                  colors: [
                    Color.fromARGB(255, 56, 49, 68), // Top-left color
                    Color.fromARGB(255, 49, 44, 60), // Bottom-left color
                    Color.fromARGB(255, 59, 51, 70), // Top-right color
                    Color.fromARGB(255, 53, 46, 63), // Bottom-right color
                  ],
                ),
              ),
              child: Column(
                children: [
                  Container(
                    child: Text(
                      "BATTLEBLADE",
                      style: TextStyle(
                        color: Color.fromARGB(255, 207, 128, 86),
                        fontSize: 40,
                        fontWeight: FontWeight.bold,
                        fontFamily: GoogleFonts.silkscreen().fontFamily,
                      ),
                    ),
                    margin: EdgeInsets.only(bottom: 10.0, top: 10.0),
                  ),
                  Container(
                    child: Text(
                      "JOIN THE BATTLE",
                      style: TextStyle(
                        color: Color.fromARGB(255, 15, 196, 163),
                        fontFamily: GoogleFonts.poppins().fontFamily,
                        fontSize: 15,
                      ),
                    ),
                    margin: EdgeInsets.only(bottom: 30.0),
                  ),
                  Center(
                    child: GestureDetector(
                      onTap: () {
                        Navigator.pushNamed(context, '/route2');
                        print("Welcome");
                      },
                      child: ClipRRect(
                        borderRadius: BorderRadius.circular(20.0),
                        child: Container(
                          margin: EdgeInsets.only(bottom: 0.0),
                          decoration: BoxDecoration(
                              border: GradientBoxBorder(
                                gradient: LinearGradient(colors: [
                                  Color.fromARGB(255, 35, 182, 155),
                                  Color.fromARGB(255, 206, 205, 45),
                                  Color.fromARGB(255, 26, 226, 46),
                                ]),
                                width: 4,
                              ),
                              borderRadius: BorderRadius.circular(25)),
                          child: Padding(
                            padding: EdgeInsets.fromLTRB(40.0, 13.0, 40.0, 13.0),
                            child: Text(
                              "Get Started",
                              style: TextStyle(
                                color: Colors.white,
                                fontFamily: GoogleFonts.poppins().fontFamily,
                                fontWeight: FontWeight.bold
                              ),
                              
                            ),
                          ),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
            Align(
              alignment: Alignment.bottomLeft,
              child: Container(
                margin: EdgeInsets.only(bottom: 0.0),
                height: deviceWidth *
                    0.68, // Adjust the height as per your requirement
                width: deviceWidth * 1.0,
                decoration: BoxDecoration(
                  image: DecorationImage(
                    image: AssetImage(
                        'C:\\Users\\dell\\StudioProjects\\untitled\\build\\flutter_assets\\bottom.png'), // Update image path accordingly
                    fit: BoxFit.fill,
                  ),
                ),
              ),
            ),
          ],
        ),
      ),  
    );
  }
}
