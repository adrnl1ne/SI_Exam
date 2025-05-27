from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import asyncio
import json
from datetime import datetime

app = FastAPI(
    title="SSE Example Server",
    description="A simple server that sends Server-Sent Events (SSE) with the current timestamp every 5 seconds.",
    version="1.0.0",
)

# Add CORS middleware to allow client connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (adjust as needed)
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/client", StaticFiles(directory="client"), name="client")

@app.get("/")
async def root():
    return {
        "message": "Welcome to the SSE Example Server!",
        "sse_endpoint": "/sse",
        "client_page": "Open the client page at client/index.html to see the SSE in action."
    }

@app.get("/sse")
async def sse():
    async def event_generator():
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message = {"timestamp": timestamp, "message": "Hello from the server!"}
            yield f"data: {json.dumps(message)}\n\n"
            await asyncio.sleep(5)

    return StreamingResponse(event_generator(), media_type="text/event-stream")