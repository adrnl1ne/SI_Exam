from pathlib import Path
import yaml
import xml.etree.ElementTree as ET
import json
import csv
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Define the base directory (should point to Mandatory_1/)
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DATA_DIR = BASE_DIR / "data"

def parse_file(set_name: str, file_type: str) -> dict:
    file_path = DATA_DIR / set_name / f"{set_name}.{file_type}"
    
    logger.debug(f"Attempting to access file: {file_path}")
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if file_type == "txt":
        return parse_text(file_path)
    elif file_type == "xml":
        return parse_xml(file_path)
    elif file_type == "yaml":
        return parse_yaml(file_path)
    elif file_type == "json":
        return parse_json(file_path)
    elif file_type == "csv":
        return parse_csv(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

def parse_text(file_path: Path) -> dict:
    result = {}
    with open(file_path, "r") as f:
        for line in f:
            key, value = line.strip().split(": ", 1)
            result[key] = value
    return result

def parse_xml(file_path: Path) -> dict:
    tree = ET.parse(file_path)
    root = tree.getroot()
    result = {}
    for child in root:
        result[child.tag] = child.text
    return result

def parse_yaml(file_path: Path) -> dict:
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

def parse_json(file_path: Path) -> dict:
    with open(file_path, "r") as f:
        return json.load(f)

def parse_csv(file_path: Path) -> dict:
    result = {}
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            return row  # Assuming one row of data
    return result