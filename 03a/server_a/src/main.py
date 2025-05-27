# 03a/server_a/src/main.py
from fastapi import FastAPI, HTTPException, Query
from typing import Dict, Any
import httpx
from .parser import parse_file  # Import the parse_file function from parser.py

app = FastAPI()

# Define the available sets and file types
SETS = ["books", "movies"]
FILE_TYPES = ["txt", "xml", "yaml", "json", "csv"]
SERVER_B_URL = "http://localhost:3000"  # Server B (Go) URL

@app.get("/")
async def root() -> Dict[str, Any]:
    """Root endpoint to display a welcome message and available options."""
    return {
        "message": "Welcome to the Data Parsing Server (Server A - FastAPI)!",
        "available_sets": SETS,
        "available_formats": FILE_TYPES
    }

@app.get("/parse/{set_name}/{file_type}")
async def parse(set_name: str, file_type: str, direct: bool = Query(False)) -> Dict[str, Any]:
    """
    Parse a specific file for a given set and file type.
    - If direct=true, parse the file directly on Server A.
    - Otherwise, forward the request to Server B.
    """
    # Validate set_name
    if set_name not in SETS:
        raise HTTPException(status_code=400, detail=f"Invalid set name. Available sets: {SETS}")

    # Validate file_type
    if file_type not in FILE_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid file type. Available types: {FILE_TYPES}")

    # If direct=true, parse the file directly
    if direct:
        try:
            data = parse_file(set_name, file_type)
            return {"set": set_name, "format": file_type, "data": data}
        except FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error parsing file: {str(e)}")

    # Otherwise, fetch from Server B
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{SERVER_B_URL}/parse/{set_name}/{file_type}?direct=true")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.json().get("detail", str(e)))
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Error communicating with Server B: {str(e)}")

@app.get("/parse/{set_name}")
async def parse_all(set_name: str, direct: bool = Query(False)) -> Dict[str, Any]:
    """
    Parse all files for a given set in all available formats.
    - If direct=true, parse the files directly on Server A.
    - Otherwise, forward the request to Server B.
    """
    # Validate set_name
    if set_name not in SETS:
        raise HTTPException(status_code=400, detail=f"Invalid set name. Available sets: {SETS}")

    # If direct=true, parse all files directly
    if direct:
        result = {}
        for file_type in FILE_TYPES:
            try:
                data = parse_file(set_name, file_type)
                result[file_type] = data
            except FileNotFoundError as e:
                result[file_type] = {"error": str(e)}
            except Exception as e:
                result[file_type] = {"error": f"Error parsing file: {str(e)}"}
        return {"set": set_name, "data": result}

    # Otherwise, fetch from Server B
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{SERVER_B_URL}/parse/{set_name}?direct=true")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.json().get("detail", str(e)))
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Error communicating with Server B: {str(e)}")