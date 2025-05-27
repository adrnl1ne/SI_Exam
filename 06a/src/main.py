from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import asyncio
from datetime import datetime
import logging

# Initialize the FastAPI app
app = FastAPI(
    title="WebSocket Example Server",
    description="A simple server that demonstrates WebSocket communication by sending periodic messages and echoing client messages.",
    version="1.0.0",
)

# Configure logging
logging.basicConfig(level=logging.INFO)

# HTML content embedded as a string
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WebSocket Example Client</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        #messages {
            border: 1px solid #ccc;
            padding: 10px;
            min-height: 200px;
            max-width: 600px;
            overflow-y: auto;
        }
        .message {
            margin-bottom: 10px;
        }
        .server-message {
            color: blue;
        }
        .client-message {
            color: green;
        }
        .error-message {
            color: red;
        }
    </style>
</head>
<body>
    <h1>WebSocket Example</h1>
    <p>Connecting to the WebSocket server. Messages will appear below.</p>
    <div>
        <input type="text" id="messageInput" placeholder="Type a message to send..." />
        <button onclick="sendMessage()">Send</button>
    </div>
    <div id="messages"></div>

    <script>
        // Dynamically set the WebSocket URL
        const wsUrl = `ws://${window.location.host}/ws`;
        const ws = new WebSocket(wsUrl);

        // Handle WebSocket connection open
        ws.onopen = function() {
            console.log('WebSocket connection opened.');
            addMessage('Connected to the server!', 'server-message');
        };

        // Handle incoming messages from the server
        ws.onmessage = function(event) {
            try {
                // Parse the data field (it's a JSON string)
                const data = JSON.parse(event.data);
                addMessage(`[${data.timestamp}] ${data.message}`, 'server-message');
            } catch (e) {
                console.error('Error parsing message:', e);
                addMessage(`Error: ${event.data}`, 'error-message');
            }
        };

        // Handle WebSocket connection errors
        ws.onerror = function(error) {
            console.error('WebSocket error:', error);
            addMessage('WebSocket error occurred.', 'error-message');
        };

        // Handle WebSocket connection close
        ws.onclose = function() {
            console.log('WebSocket connection closed.');
            addMessage('Disconnected from the server.', 'error-message');
        };

        // Function to send a message to the server
        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            if (message && ws.readyState === WebSocket.OPEN) {
                ws.send(message);
                addMessage(`You: ${message}`, 'client-message');
                input.value = ''; // Clear the input field
            } else if (ws.readyState !== WebSocket.OPEN) {
                addMessage('Cannot send message: WebSocket is not connected.', 'error-message');
            }
        }

        // Function to add a message to the messages div
        function addMessage(text, className) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${className}`;
            messageDiv.textContent = text;
            document.getElementById('messages').appendChild(messageDiv);
            // Scroll to the bottom of the messages div
            document.getElementById('messages').scrollTop = document.getElementById('messages').scrollHeight;
        }

        // Allow sending messages by pressing Enter
        document.getElementById('messageInput').addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the HTML client."""
    return HTML_CONTENT

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handle WebSocket connections."""
    await websocket.accept()
    try:
        while True:
            # Wait for a message from the client
            client_message = await websocket.receive_text()
            # Echo the message back to the client as JSON
            response = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "message": f"Server received: {client_message}"
            }
            await websocket.send_json(response)  # Send as JSON
    except WebSocketDisconnect:
        print("WebSocket connection closed.")