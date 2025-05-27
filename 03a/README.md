# 03a - Data Parsing Servers Implementation

## Overview
This directory contains the implementation of two data parsing servers that can parse data files in various formats (`txt`, `xml`, `yaml`, `json`, `csv`) for two sets (`books`, `movies`):
- **Server A (FastAPI, Python):** Parses data files directly or forwards requests to Server B when `direct=false`. Runs on `http://127.0.0.1:8000`.
- **Server B (Go):** Parses the same data files directly or forwards requests to Server A when `direct=false`. Runs on `http://localhost:3000`.

The servers communicate over HTTP, allowing them to forward requests to each other based on the `direct` query parameter. The data files are stored in `Mandatory_1/data/`, with subdirectories `books/` and `movies/` containing the files in the supported formats (e.g., `books/books.txt`, `movies/movies.yaml`).

## Setup Instructions

### Prerequisites
- **Python 3.12+** and **Poetry** (for Server A).
- **Go 1.21+** (for Server B).
- Ensure the `data/` directory exists in the root (`Mandatory_1/data/`) with `books/` and `movies/` subdirectories containing the data files.

### Installation and Running the Servers

#### Server A (FastAPI, Python)
1. Navigate to the `server_a` directory:
    ```bash
    cd 03a/server_a
    ```
2. Install dependencies using Poetry:
    ```bash
    poetry install
    ```
3. Run the server:
    ```bash
    poetry run start
    ```
   This starts Server A on `http://127.0.0.1:8000`. Access the interactive API documentation at `http://127.0.0.1:8000/docs`.

#### Server B (Go)
1. Navigate to the `server_b` directory:
    ```bash
    cd 03a/server_b
    ```
2. Install the `swag` tool for Swagger documentation:
    ```bash
    go install github.com/swaggo/swag/cmd/swag@latest
    ```
3. Generate Swagger documentation:
    ```bash
    swag init
    ```
4. Run the server:
    ```bash
    go run .
    ```
   This starts Server B on `http://localhost:3000`. Access the interactive Swagger UI at `http://localhost:3000/swagger/index.html`.

**Note:** Both servers must be running simultaneously for request forwarding to work.

## API Usage Examples

### Common Endpoints
- **Root Endpoint:** Get a welcome message with available sets and formats.
  - Server A: `http://127.0.0.1:8000/`
  - Server B: `http://localhost:3000/`
  - Example Response:
    ```json
    {
      "message": "Welcome to the Data Parsing Server!",
      "available_sets": ["books", "movies"],
      "available_formats": ["txt", "xml", "yaml", "json", "csv"]
    }
    ```

- **Parse a Specific File:** Parse a file for a given set and format.
  - Server A (direct): `http://127.0.0.1:8000/parse/books/txt?direct=true`
  - Server B (direct): `http://localhost:3000/parse/books/txt?direct=true`
  - Example Response:
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
  - Use `direct=false` to forward the request to the other server:
    - Server A → Server B: `http://127.0.0.1:8000/parse/books/txt?direct=false`
    - Server B → Server A: `http://localhost:3000/parse/books/txt?direct=false`

- **Parse All Files for a Set:** Parse all files for a given set in all formats.
  - Server A (direct): `http://127.0.0.1:8000/parse/books?direct=true`
  - Server B (direct): `http://localhost:3000/parse/books?direct=true`
  - Example Response:
    ```json
    {
      "set": "books",
      "data": {
        "txt": {
          "Title": "The Hobbit",
          "Author": "J.R.R. Tolkien",
          "Year": "1937",
          "Genre": "Fantasy"
        },
        "xml": {
          "Title": "The Hobbit",
          "Author": "J.R.R. Tolkien",
          "Year": "1937",
          "Genre": "Fantasy"
        },
        "yaml": {
          "book": {
            "title": "The Hobbit",
            "author": "J.R.R. Tolkien",
            "year": 1937,
            "genre": "Fantasy"
          }
        },
        "json": {
          "title": "The Hobbit",
          "author": "J.R.R. Tolkien",
          "year": 1937,
          "genre": "Fantasy"
        },
        "csv": {
          "Title": "The Hobbit",
          "Author": "J.R.R. Tolkien",
          "Year": "1937",
          "Genre": "Fantasy"
        }
      }
    }
    ```
  - Use `direct=false` to forward the request to the other server:
    - Server A → Server B: `http://127.0.0.1:8000/parse/books?direct=false`
    - Server B → Server A: `http://localhost:3000/parse/books?direct=false`

## Troubleshooting

- **File Not Found Errors:**
  - Ensure the `data/` directory exists in the root (`Mandatory_1/data/`).
  - Check the `BASE_DIR` in `server_a/src/parser.py`:
    ```python
    BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
    ```
  - Check the `BaseDir` in `server_b/parser/parser.go`:
    ```go
    BaseDir = filepath.Join(dir, "..", "..", "data")
    ```

- **Communication Errors:**
  - Ensure both servers are running simultaneously.
  - Verify the URLs used for forwarding requests:
    - Server A → Server B: `http://localhost:3000`
    - Server B → Server A: `http://127.0.0.1:8000`

- **Swagger UI Fails to Load (Server B):**
  - Regenerate Swagger documentation:
    ```bash
    cd 03a/server_b
    swag init
    ```

- **Go Import Errors (Server B):**
  - Ensure the module name in `go.mod` matches the imports in `main.go`.

## Notes
- Both servers must be running for full functionality.
- Ensure the `data/` directory is properly structured and accessible.

## Author
**Name**: Jakob Helander
**Email**: jako7096@stud.kea.dk