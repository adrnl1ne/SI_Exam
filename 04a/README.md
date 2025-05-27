# 04a - SSE Example Server

## Overview
This project implements a simple **Server-Sent Events (SSE)** server using **FastAPI**. The server streams timestamped messages to connected clients every 5 seconds. A basic HTML client is included to demonstrate the functionality.

---

## Project Structure
- `src/`: Contains the FastAPI server implementation.
    - `main.py`: The main server file with the SSE endpoint.
- `client/`: Contains the HTML client to connect to the SSE server.
    - `index.html`: A simple web page to display SSE messages.
- `pyproject.toml`: Python project configuration file for dependencies.

---

## Prerequisites
- **Python 3.12+**: Ensure Python is installed on your system.
- **Poetry**: Install Poetry for dependency management.

---

## Setup Instructions

### Install Dependencies
1. Navigate to the `04a` directory:
    ```bash
    cd path/to/04a
    ```
2. Install the required dependencies using Poetry:
    ```bash
    poetry install
    ```

---

## Running the Server
1. Start the FastAPI server:
    ```bash
    poetry run uvicorn src.main:app --host 127.0.0.1 --port 8002 --reload
    ```
2. Access the server:
    - **Root Endpoint:** [http://127.0.0.1:8002/](http://127.0.0.1:8002/)
    - **SSE Endpoint:** [http://127.0.0.1:8002/sse](http://127.0.0.1:8002/sse)
    - **Client Page:** [http://127.0.0.1:8002/client/index.html](http://127.0.0.1:8002/client/index.html)

---

## Features

### Endpoints
- **GET /**: Returns a welcome message with links to the SSE endpoint and client page.
- **GET /sse**: Streams timestamped messages to connected clients every 5 seconds.

### Client
- The `index.html` file connects to the `/sse` endpoint and displays incoming messages in real-time.

---

## Troubleshooting
- **Port Conflicts:** If port `8002` is in use, start the server on a different port:
    ```bash
    poetry run uvicorn src.main:app --host 127.0.0.1 --port 8003 --reload
    ```
    Update the `EventSource` URL in `client/index.html` to match the new port:
    ```javascript
    const source = new EventSource('http://localhost:8003/sse');
    ```

- **CORS Issues:** The server is configured to allow all origins using CORS middleware. Adjust the `allow_origins` parameter in `main.py` if needed.

---

## Author
**Name**: Jakob Helander
**Email**: jako7096@stud.kea.dk