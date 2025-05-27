# src/parser.py
import json
import csv
import xml.etree.ElementTree as ET
import yaml
from pathlib import Path
from typing import Dict, Any

# Base directory for files (relative to project root)
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # Adjusted to point to Mandatory_1

def parse_text(file_path: Path) -> Dict[str, str]:
    """Parse a text file into a dictionary."""
    data = {}
    with open(file_path, 'r') as file:
        for line in file:
            if ': ' in line:
                key, value = line.strip().split(': ', 1)
                data[key] = value
    return data

def parse_xml(file_path: Path) -> Dict[str, str]:
    """Parse an XML file into a dictionary."""
    tree = ET.parse(file_path)
    root = tree.getroot()
    data = {}
    for child in root:
        data[child.tag] = child.text
    return data

def parse_yaml(file_path: Path) -> Dict[str, Any]:
    """Parse a YAML file into a dictionary."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def parse_json(file_path: Path) -> Dict[str, Any]:
    """Parse a JSON file into a dictionary."""
    with open(file_path, 'r') as file:
        return json.load(file)

def parse_csv(file_path: Path) -> Dict[str, str]:
    """Parse a CSV file into a dictionary."""
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        return next(reader)  # Assuming one row for simplicity

def parse_file(set_name: str, file_type: str) -> Dict[str, Any]:
    """Parse a file based on its type and set name."""
    # File path is now data/{set_name}/{set_name}.{file_type}
    file_path = BASE_DIR / "data" / set_name / f"{set_name}.{file_type}"
    
    if not file_path.exists():
        raise FileNotFoundError(f"File {file_path} not found")

    if file_type == 'txt':
        return parse_text(file_path)
    elif file_type == 'xml':
        return parse_xml(file_path)
    elif file_type == 'yaml':
        return parse_yaml(file_path)
    elif file_type == 'json':
        return parse_json(file_path)
    elif file_type == 'csv':
        return parse_csv(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")