from fastapi import FastAPI, HTTPException
from src.parser import parse_file
from pydantic import BaseModel
from typing import Dict, Any, List

class RootResponse(BaseModel):
    message: str
    available_sets: List[str]
    available_formats: List[str]

class ParseResponse(BaseModel):
    set: str
    format: str
    data: Dict[str, Any]

class ParseAllResponse(BaseModel):
    set: str
    data: Dict[str, Dict[str, Any]]

app = FastAPI(
    title="Data Parsing Server",
    description="A FastAPI server to parse data files in multiple formats.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "General",
            "description": "General endpoints for the server."
        },
        {
            "name": "Parsing",
            "description": "Endpoints for parsing data files."
        }
    ]
)

SETS = ["books", "movies"]
FILE_TYPES = ["txt", "xml", "yaml", "json", "csv"]

@app.get("/", response_model=RootResponse, tags=["General"])
async def root():
    """Root endpoint with a welcome message."""
    return {
        "message": "Welcome to the Data Parsing Server!",
        "available_sets": SETS,
        "available_formats": FILE_TYPES
    }

@app.get("/parse/{set_name}/{file_type}", response_model=ParseResponse, tags=["Parsing"])
async def parse(set_name: str, file_type: str):
    """
    Parse a specific file from a set and return its data.
    
    Args:
        set_name: The name of the set (e.g., 'books' or 'movies')
        file_type: The file format (e.g., 'txt', 'xml', 'yaml', 'json', 'csv')
    
    Returns:
        The parsed data as a dictionary.
    """
    # Validate set_name
    if set_name not in SETS:
        raise HTTPException(status_code=400, detail=f"Invalid set name. Available sets: {SETS}")
    
    # Validate file_type
    if file_type not in FILE_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid file type. Available types: {FILE_TYPES}")
    
    try:
        data = parse_file(set_name, file_type)
        return {
            "set": set_name,
            "format": file_type,
            "data": data
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing file: {str(e)}")

@app.get("/parse/{set_name}", response_model=ParseAllResponse, tags=["Parsing"])
async def parse_all(set_name: str):
    """
    Parse all files in a set and return their data.
    
    Args:
        set_name: The name of the set (e.g., 'books' or 'movies')
    
    Returns:
        A dictionary with the parsed data for each file type.
    """
    if set_name not in SETS:
        raise HTTPException(status_code=400, detail=f"Invalid set name. Available sets: {SETS}")
    
    result = {}
    for file_type in FILE_TYPES:
        try:
            data = parse_file(set_name, file_type)
            result[file_type] = data
        except FileNotFoundError:
            result[file_type] = {"error": f"File {set_name}.{file_type} not found"}
        except Exception as e:
            result[file_type] = {"error": f"Error parsing file: {str(e)}"}
    
    return {
        "set": set_name,
        "data": result
    }