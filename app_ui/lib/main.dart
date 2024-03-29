import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:flutter/services.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
    DeviceOrientation.portraitDown,
  ]);
  runApp(const MyApp(title: 'My App'));
}

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
      body: SingleChildScrollView(
        child: Column(
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
                "Enter gaming device IP address",
                style: TextStyle(
                  color: Colors.black,
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  fontFamily: GoogleFonts.poppins().fontFamily,
                ),
              ),
              color: Color.fromARGB(255, 255, 255, 255),
              
              margin: EdgeInsets.only(top: 50.0,bottom: 10.0),
            ),  
            MyCustomForm(),
            
            
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

// Create a corresponding State class.
// This class holds data related to the form.
class MyCustomFormState extends State<MyCustomForm> {
  final TextEditingController _textController = TextEditingController();
  final _formKey = GlobalKey<FormState>(); 
  // Rest of your code...

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
              controller: _textController, // Assign controller to the TextFormField
              decoration: InputDecoration(
                border: OutlineInputBorder(
                  borderSide: const BorderSide(color: Colors.amber, width: 4),
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
              // The validator receives the text that the user has entered.
              validator: (value) {
                print(value);
                if (value == null || value.isEmpty) {
                  return 'Please enter some text';
                }
                return null;
              },
            ),
          ),
          Container(
            margin: EdgeInsets.only(top: 20.0),
            child: Center(
              child: ElevatedButton(
                onPressed: () {
                  print("Welcome");
                  // Validate returns true if the form is valid, or false otherwise.
                  if (_formKey.currentState!.validate()) {
                    // If the form is valid, clear text field and display a snackbar.
                    _textController.clear(); // Clear text field
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('Processing Data')),
                    );
                  }
                },
                child: Padding(
                  padding: EdgeInsets.fromLTRB(40.0, 12.0, 40.0, 12.0),
                  child: Text("Submit"),
                ),
                style: ButtonStyle(
                  backgroundColor: MaterialStateProperty.all<Color>(Color.fromARGB(255, 98, 100, 228)),
                  foregroundColor: MaterialStateProperty.all<Color>(Color.fromARGB(255, 255, 255, 255)),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

