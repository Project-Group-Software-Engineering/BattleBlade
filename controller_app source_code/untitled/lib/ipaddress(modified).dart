import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:flutter/services.dart';
import 'package:gradient_borders/box_borders/gradient_box_border.dart';
import 'decrypt.dart';
import 'package:rflutter_alert/rflutter_alert.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

class ippage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    
    double deviceWidth = MediaQuery.of(context).size.width;
    return Scaffold(
      backgroundColor: Color.fromARGB(255, 255, 255, 255),
      body: SingleChildScrollView(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Align(
              alignment: Alignment.centerRight,
              child: Container(
                height: deviceWidth *
                    0.9, // Adjust the height as per your requirement
                width: deviceWidth * 1.0,
                decoration: BoxDecoration(
                  image: DecorationImage(
                    image: AssetImage(
                        'C:\\Users\\dell\\StudioProjects\\untitled\\build\\flutter_assets\\top.png'), // Update image path accordingly
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
              child: LayoutBuilder(
                builder: (context, constraints) {
                  double horizontalPadding =
                      constraints.maxWidth * 0.18; // 18% padding on both sides
                  return Padding(
                    padding:
                        EdgeInsets.symmetric(horizontal: horizontalPadding),
                    child: Column(
                      children: [
                        Container(
                          width: double.infinity, // Ensure text doesn't wrap
                          child: Text(
                            "Enter gaming device IP key",
                            style: TextStyle(
                              color: Color.fromARGB(255, 15, 196, 163),
                              fontFamily: GoogleFonts.poppins().fontFamily,
                              fontSize: 20,
                              fontWeight: FontWeight.bold,
                            ),
                            textAlign: TextAlign.center,
                          ),
                          margin: EdgeInsets.only(bottom: 10.0),
                        ),
                        MyCustomForm(),
                      ],
                    ),
                  );
                },
              ),
            ),
            Align(
              alignment: Alignment.bottomLeft,
              child: Container(
                padding: EdgeInsets.all(0.0),
                margin: EdgeInsets.all(0.0),
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

class MyCustomForm extends StatefulWidget {
  const MyCustomForm({super.key});

  @override
  MyCustomFormState createState() {
    return MyCustomFormState();
  }
}

late String cipherText;
late String decryptedText;
int success = 0;

// Create a corresponding State class.
// This class holds data related to the form.
class MyCustomFormState extends State<MyCustomForm> {
  final TextEditingController _textController = TextEditingController();
  final _formKey = GlobalKey<FormState>();
  late WebSocketChannel _channel;
  

  int _connectWebSocket(String decryptedText) {
    // Get the IP address from the text field
    String ipAddress = decryptedText;
    print(ipAddress);

    _channel = WebSocketChannel.connect(
      Uri.parse('ws://$ipAddress:8765'),
    );
    _channel.sink.add("Trying to establish flutter connection");
    print("added");

    // Listen for messages from the WebSocket channel
    _channel.stream.listen(
      (message) {
        print('Received message: $message');
        success = 1;
        Alert(
            context: context,
            title: "SUCCESS",
            desc: "Connected successfully",
            image: Container(
              width: 100, // Specify the desired width
              height: 100, // Specify the desired height
              child: Image.asset(
                  'C:\\Users\\dell\\StudioProjects\\untitled\\build\\flutter_assets\\success.png'),
            ),
            buttons: [
              DialogButton(
                onPressed: () {
                  Navigator.pop(context);
                  Navigator.pushNamed(context, '/route3');// Pop the context when the "OK" button is pressed
                },
                child: Text(
                  "OK",
                  style: TextStyle(
                      color: Color.fromARGB(255, 255, 255, 255), fontSize: 20),
                ),
              ),
            ]).show();
            _textController.clear();

      },
      onError: (error) {
        print('Error occurred: $error');
        success = 0;
        Alert(
            context: context,
            title: "FAILURE",
            desc: "Please enter correct ip address key",
            image: Container(
              width: 100, 
              height: 100, 
              child: Image.asset(
                  'C:\\Users\\dell\\StudioProjects\\untitled\\build\\flutter_assets\\failure.png'),
            ),
            buttons: [
              DialogButton(
                onPressed: () {
                  Navigator.pop(
                      context);
                      
                },
                child: Text(
                  "OK",
                  style: TextStyle(
                      color: Color.fromARGB(255, 255, 255, 255), fontSize: 20),
                ),
              ),
            ]).show();
             _textController.clear();

      },
      onDone: () {
        print('Connection closed');
      },
    );
    print(success);
    return success;
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          SizedBox(
            width: 250,
            child: TextFormField(
              cursorColor: const Color.fromARGB(255, 255, 255, 255),
              controller:
                  _textController,
              style: TextStyle(
                color: const Color.fromARGB(255, 255, 255, 255),
                fontSize: 20,
                fontFamily: GoogleFonts.prompt().fontFamily,
                fontWeight: FontWeight.bold,
              ),

              decoration: InputDecoration(
                border: OutlineInputBorder(
                  borderSide: const BorderSide(
                      color: Color.fromARGB(255, 255, 255, 255), width: 4),
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
              
              validator: (value) {
                print(value);
                cipherText = value.toString(); 
                String key = "battleblade";
                String alphabet = "0123456789.abcdefghijklmnopqrstuvwxyz";
                decryptedText = decrypt(cipherText, key, alphabet);
                print("Decrypted Text: $decryptedText");
                if (value == null || value.isEmpty) {
                  return 'Please enter some text';
                }
                return null;
              },
            ),
          ),
          Container(
            margin: EdgeInsets.only(top: 20.0, left: 0.0, right: 0.0),
            child: GestureDetector(
              onTap: () {
                print("Welcome");
                
                if (_formKey.currentState!.validate()) {
                  
                  print(decryptedText);
                  
                  int result = _connectWebSocket(decryptedText);
                  print(result);
                  _textController.clear();
                  
                }
              },
              child: ClipRRect(
                borderRadius: BorderRadius.circular(20.0),
                child: Container(
                  margin: EdgeInsets.only(bottom: 24.0),
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
                      "Connect",
                      style: TextStyle(
                          color: Colors.white,
                          fontFamily: GoogleFonts.poppins().fontFamily,
                          fontWeight: FontWeight.bold),
                    ),
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
