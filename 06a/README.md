# 06a - WebSocket Example Server

## Overview
This project implements a **WebSocket server** using **FastAPI**. The server demonstrates WebSocket communication by:
- Sending periodic messages with timestamps to connected clients.
- Echoing messages received from clients back to them.

A simple HTML client is included to interact with the WebSocket server.

---

## Project Structure
- `src/`: Contains the FastAPI server implementation.
    - `main.py`: The main server file with the WebSocket endpoint.
- `pyproject.toml`: Python project configuration file for dependencies.

---

## Prerequisites
- **Python 3.12+**: Ensure Python is installed on your system.
- **Poetry**: Install Poetry for dependency management.

---

## Setup Instructions

### Install Dependencies
1. Navigate to the `06a` directory:
    ```bash
    cd path/to/06a
    ```
2. Install the required dependencies using Poetry:
    ```bash
    poetry install
    ```

---

## Running the Server
1. Start the FastAPI server:
    ```bash
    poetry run uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload
    ```
2. Access the server:
    - **Root Endpoint:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
    - **WebSocket Endpoint:** `ws://127.0.0.1:8000/ws`

---

## Features

### Endpoints
- **GET /**: Serves an HTML client to interact with the WebSocket server.
- **WebSocket /ws**: Handles WebSocket connections:
    - Listens for incoming messages from clients and echoes them back.
  

### Client
- The embedded HTML client connects to the `/ws` WebSocket endpoint and displays incoming messages in real-time.
- Users can send messages to the server using the input field.

---

## Troubleshooting
- **Port Conflicts:** If port `8000` is in use, start the server on a different port:
    ```bash
    poetry run uvicorn src.main:app --host 127.0.0.1 --port 8001 --reload
    ```
    Update the WebSocket URL in the HTML client to match the new port:
    ```javascript
    const wsUrl = `ws://${window.location.host}/ws`;
    ```

- **WebSocket Connection Issues:** Ensure the server is running and accessible at the specified host and port.

---

## Author
**Name**: Jakob Helander  
**Email**: jako7096@stud.kea.dk