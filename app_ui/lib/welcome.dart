import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:google_fonts/google_fonts.dart';

void main() => runApp(const MyApp(title: 'My App'));

class MyApp extends StatelessWidget {
  final String title;

  const MyApp({Key? key, required this.title}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
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
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color.fromARGB(255, 255, 255, 255),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Container(
	              height: 400,
	              decoration: BoxDecoration(
	                image: DecorationImage(
	                  image: AssetImage('C:\\Users\\dell\\StudioProjects\\untitled\\build\\flutter_assets\\background.png'),
	                  fit: BoxFit.fill
	                )
	              ),
          ),
          Container(
            child: Text(
              "Welcome to BattleBlade",
              style: TextStyle(
                color: Colors.black,
                fontSize: 23,
                fontWeight: FontWeight.bold,
                fontFamily: GoogleFonts.poppins().fontFamily,
              ),
            ),
            color: Color.fromARGB(255, 255, 255, 255),
            
            margin: EdgeInsets.only(bottom: 10.0),
          ),  
          Container(
            child: Text(
              "Motto of our game",
              style: TextStyle(
                color: Color.fromARGB(243, 156, 151, 151),
                fontSize: 15,
              ),
            ),
            color: Color.fromARGB(255, 255, 255, 255),
            
            margin: EdgeInsets.only(bottom: 100.0),
          ),
          
          Center(
            child: ElevatedButton(
              onPressed: (){
                print("Welcome");
              }, 
              child: Padding(
                padding: EdgeInsets.fromLTRB(40.0, 12.0, 40.0, 12.0),
                child: Text("Get Started"),
              ),
              style: ButtonStyle(
                backgroundColor: MaterialStateProperty.all<Color>(Color.fromARGB(255, 98, 100, 228)),
                foregroundColor: MaterialStateProperty.all<Color>(Color.fromARGB(255, 255, 255, 255)),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
