package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strings"

	_ "server_b/docs" // Import the generated docs package
	"server_b/parser" // Import the parser package

	httpSwagger "github.com/swaggo/http-swagger" // Swagger UI middleware
	_ "github.com/swaggo/swag"                   // Required for swag init to work
)

// ServerAURL is the URL for Server A (FastAPI)
const ServerAURL = "http://127.0.0.1:8000"

// Available sets and file types
var sets = []string{"books", "movies"}
var fileTypes = []string{"txt", "xml", "yaml", "json", "csv"}
var serverBPort = "3000"

// @title Data Parsing Server (Server B - Go)
// @version 1.0
// @description This is a data parsing server implemented in Go (Server B). It can parse data files directly or forward requests to Server A.
// @host localhost:3000
// @BasePath /
func main() {
	// Define routes
	http.HandleFunc("/", rootHandler)
	http.HandleFunc("/parse/", parseHandler)

	// Serve Swagger UI at /swagger/
	http.HandleFunc("/swagger/", httpSwagger.WrapHandler)

	log.Printf("Server B (Go) starting on http://localhost:%s", serverBPort)
	log.Printf("Swagger UI available at http://localhost:%s/swagger/index.html", serverBPort)
	if err := http.ListenAndServe(":"+serverBPort, nil); err != nil {
		log.Fatalf("Server B failed to start: %v", err)
	}
}

// rootHandler handles the root endpoint
// @Summary Get welcome message
// @Description Returns a welcome message with available sets and file types
// @Tags General
// @Produce json
// @Success 200 {object} map[string]interface{} "Welcome message"
// @Router / [get]
func rootHandler(w http.ResponseWriter, r *http.Request) {
	if r.URL.Path != "/" || r.Method != http.MethodGet {
		http.Error(w, "Not Found", http.StatusNotFound)
		return
	}

	response := map[string]interface{}{
		"message":           "Welcome to the Data Parsing Server (Server B - Go)!",
		"available_sets":    sets,
		"available_formats": fileTypes,
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

// parseHandler handles parsing requests
// @Summary Parse a specific file or all files for a set
// @Description Parses a file for a given set and file type, or all files for a set. If direct=true, parses directly; otherwise, forwards to Server A.
// @Tags Parsing
// @Produce json
// @Param set_name path string true "Set name (e.g., books, movies)"
// @Param file_type path string false "File type (e.g., txt, xml, yaml, json, csv)"
// @Param direct query bool false "Whether to parse directly (default: false)"
// @Success 200 {object} map[string]interface{} "Parsed data"
// @Failure 400 {string} string "Invalid set name or file type"
// @Failure 404 {string} string "File not found"
// @Failure 500 {string} string "Internal server error"
// @Router /parse/{set_name}/{file_type} [get]
// @Router /parse/{set_name} [get]
func parseHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
		return
	}

	// Extract path components: /parse/{set_name}/{file_type} or /parse/{set_name}
	pathParts := strings.Split(strings.Trim(r.URL.Path, "/"), "/")
	if len(pathParts) < 2 || pathParts[0] != "parse" {
		http.Error(w, "Invalid path", http.StatusBadRequest)
		return
	}

	setName := pathParts[1]
	var fileType string
	parseAll := false

	if len(pathParts) == 2 {
		// /parse/{set_name} -> parse all file types for the set
		parseAll = true
	} else if len(pathParts) == 3 {
		// /parse/{set_name}/{file_type}
		fileType = pathParts[2]
	} else {
		http.Error(w, "Invalid path", http.StatusBadRequest)
		return
	}

	// Validate set name
	if !contains(sets, setName) {
		http.Error(w, fmt.Sprintf("Invalid set name. Available sets: %v", sets), http.StatusBadRequest)
		return
	}

	// Validate file type if provided
	if !parseAll && !contains(fileTypes, fileType) {
		http.Error(w, fmt.Sprintf("Invalid file type. Available types: %v", fileTypes), http.StatusBadRequest)
		return
	}

	// Check if direct=true
	direct := r.URL.Query().Get("direct") == "true"

	if direct {
		// Parse directly on Server B
		if parseAll {
			// Parse all file types for the set
			result := make(map[string]interface{})
			for _, ft := range fileTypes {
				data, err := parser.ParseFile(setName, ft)
				if err != nil {
					result[ft] = map[string]string{"error": err.Error()}
				} else {
					result[ft] = data
				}
			}
			respondJSON(w, map[string]interface{}{"set": setName, "data": result})
		} else {
			// Parse a specific file
			data, err := parser.ParseFile(setName, fileType)
			if err != nil {
				http.Error(w, err.Error(), http.StatusInternalServerError)
				return
			}
			respondJSON(w, map[string]interface{}{"set": setName, "format": fileType, "data": data})
		}
	} else {
		// Forward request to Server A
		client := &http.Client{}
		// Trim the leading slash from r.URL.Path to avoid double slashes
		path := strings.TrimLeft(r.URL.Path, "/")
		url := fmt.Sprintf("%s/%s?direct=true", ServerAURL, path)
		resp, err := client.Get(url)
		if err != nil {
			http.Error(w, fmt.Sprintf("Error communicating with Server A: %v", err), http.StatusInternalServerError)
			return
		}
		defer resp.Body.Close()

		var response map[string]interface{}
		if err := json.NewDecoder(resp.Body).Decode(&response); err != nil {
			http.Error(w, fmt.Sprintf("Error decoding response from Server A: %v", err), http.StatusInternalServerError)
			return
		}

		if resp.StatusCode != http.StatusOK {
			http.Error(w, fmt.Sprintf("Server A error: %v", response["detail"]), resp.StatusCode)
			return
		}

		respondJSON(w, response)
	}
}

// Helper function to check if a slice contains a string
func contains(slice []string, item string) bool {
	for _, s := range slice {
		if s == item {
			return true
		}
	}
	return false
}

// Helper function to respond with JSON
func respondJSON(w http.ResponseWriter, data interface{}) {
	w.Header().Set("Content-Type", "application/json")
	if err := json.NewEncoder(w).Encode(data); err != nil {
		http.Error(w, fmt.Sprintf("Error encoding response: %v", err), http.StatusInternalServerError)
	}
}
