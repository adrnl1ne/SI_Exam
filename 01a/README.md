# 01a: Data Parsing Server

This project implements a data parsing server in Python (FastAPI) and JavaScript (Express). It parses data files in multiple formats (txt, xml, yaml, json, csv) for two sets—books and movies—and exposes the data via HTTP endpoints. Both implementations provide interactive API documentation through Swagger UI.

## Prerequisites
- **Python 3.12+**: Install Python 3.12 or higher.
- **Poetry**: Install Poetry for Python dependency management.
- **Node.js and npm**: Install Node.js.

## Project Structure
- `src/`: Python implementation (FastAPI).
    - `main.py`: FastAPI application.
    - `parser.py`: Parsing logic.
- `js/`: JavaScript implementation (Express).
    - `server.js`: Express application.
    - `parser.js`: Parsing logic.
- `data/`: Data files for books and movies in various formats.
- `pyproject.toml`: Python dependencies configuration.
- `js/package.json`: JavaScript dependencies configuration.

## Python Implementation (FastAPI)

### Setup
1. Navigate to the project directory:
    ```bash
    cd path/to/01a
    ```
2. Install dependencies:
    ```bash
    poetry install
    ```
3. (Optional) Activate the virtual environment:
    ```bash
    poetry shell
    ```

### Running the Server
- Start the server:
    ```bash
    poetry run start
    ```
- For development with auto-reload:
    ```bash
    poetry run uvicorn src.main:app --reload
    ```
- Access the API:
    - Root: [http://127.0.0.1:8000](http://127.0.0.1:8000)
    - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)


## JavaScript Implementation (Express)

### Setup
1. Navigate to the JavaScript directory:
    ```bash
    cd path/to/01a/js
    ```
2. Install dependencies:
    ```bash
    npm install
    ```

### Running the Server
- Start the server:
    ```bash
    npm start
    ```
- For development with auto-reload:
    ```bash
    npm run dev
    ```
- Access the API:
    - Root: [http://localhost:3000](http://localhost:3000)
    - Swagger UI: [http://localhost:3000/api-docs](http://localhost:3000/api-docs)

## API Endpoints
### Common Endpoints
- **GET /**: Welcome message with available sets and formats.
- **GET /parse/{set_name}/{file_type}**: Parse a specific file from a set.
- **GET /parse/{set_name}**: Parse all files in a set.

### Example Response
```json
{
    "set": "books",
    "format": "txt",
    "data": {
        "Title": "The Hobbit",
        "Author": "J.R.R. Tolkien",
        "Year": "1937",
        "Genre": "Fantasy"
    }
}
```

## Troubleshooting
- **Poetry Install Fails**: Update Poetry:
    ```bash
    poetry self update
    ```
- **npm Install Fails**: Clear npm cache:
    ```bash
    npm cache clean --force
    npm install
    ```
- **Port Issues**:
    - Python: Use a different port:
        ```bash
        poetry run uvicorn src.main:app --port 8001 --reload
        ```
    - JavaScript: Modify `server.js` to use a different port.

## Author
**Name**: Jakob Helander
**Email**: jako7096@stud.kea.dk
