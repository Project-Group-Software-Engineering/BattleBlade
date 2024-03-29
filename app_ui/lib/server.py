import asyncio
import websockets


# Define the WebSocket server
async def handle_connection(websocket, path):
    print("Connection estabilished")
    await websocket.send("Welcome! You are connected to the laptop hotspot.")
    try:
        async for message in websocket:
            print("Received message: ", message)
            # Perform actions when the event is received
            # For example, you can send a response back to the client if needed
            await websocket.send("Connected to laptop")
    except websockets.exceptions.ConnectionClosedOK:
        print("WebSocket connection closed")
    # Simulate mobile device connecting
    # await asyncio.sleep(5)
    # await websocket.send("coṇnnected")


start_server = websockets.serve(handle_connection, "10.81.33.167", 5000)

# Start the server
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
