Elevated button

child: ElevatedButton(
          onPressed: (){
            print("Pressed Elevated button");
          },
          child: Text('Click me'),
          style: ButtonStyle(
            backgroundColor: MaterialStateProperty.all<Color>(Colors.blue),
            foregroundColor: MaterialStateProperty.all<Color>(const Color.fromARGB(255, 0, 0, 0)),
          ),
        ),


Elevated button with icon
child: ElevatedButton.icon(
          onPressed: (){}, 
          icon: Icon(
            Icons.mail
          ), 
          label: Text("Mail me"),
          style: ButtonStyle(
            backgroundColor: MaterialStateProperty.all<Color>(Colors.amber),
            foregroundColor: MaterialStateProperty.all<Color>(const Color.fromARGB(255, 0, 0, 0)),
          ),
        ),

Container
body: Container(
        color: Colors.lightBlue,
        child: Text("hello"),
        padding: EdgeInsets.all(20.0),
        margin: EdgeInsets.all(10.0),
      ),


Row
body: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Text("Hello world"),
          TextButton(
            onPressed: (){}, 
            child: Text("Click me"),
            style: ButtonStyle(
            backgroundColor: MaterialStateProperty.all<Color>(Colors.amber),
            foregroundColor: MaterialStateProperty.all<Color>(const Color.fromARGB(255, 0, 0, 0)),
          ),
          ),
          Container(
            color: Colors.cyan,
            padding: EdgeInsets.all(10),
            child: Text("inside container"),
          )
        ],
      ),


Column

Column(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            padding: EdgeInsets.all(20.0),
            color: Colors.cyan,
            child: Text('One'),
          ),
          Container(
            padding: EdgeInsets.all(30.0),
            color: Colors.pinkAccent,
            child: Text('Two'),
          ),
          Container(
            padding: EdgeInsets.all(30.0),
            color: Colors.amber,
            child: Text('Three'),
          ),
        ],
      ),


Expanded widget

body: Row(
        children: [
          Expanded(
            flex: 3,
            child: Container(
              padding: EdgeInsets.all(30.0),
              color: Colors.cyan,
              child: Text('1'),
            ),
          ),
          
          Expanded(
            flex: 2,
            child: Container(
              padding: EdgeInsets.all(30.0),
              color: Colors.pinkAccent,
              child: Text('2'),
            ),
          ),
          Expanded(
            flex: 1,
            child: Container(
              padding: EdgeInsets.all(30.0),
              color: Colors.amber,
              child: Text('3'),
            ),
          ),
        ],
      ),