package parser

import (
	"encoding/csv"
	"encoding/json"
	"encoding/xml"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"gopkg.in/yaml.v3"
)

// BaseDir points to the root directory (Mandatory 1/)
var BaseDir string

func init() {
	// Get the directory of parser.go
	dir, err := os.Getwd()
	if err != nil {
		panic(fmt.Sprintf("failed to get working directory: %v", err))
	}
	// Navigate up to Mandatory_1/ and then to data/
	// From 03a/server_b/, we need to go up two directories: server_b/ -> 03a/ -> Mandatory_1/
	BaseDir = filepath.Join(dir, "..", "..", "data")
	// Resolve to absolute path to avoid relative path issues
	BaseDir, err = filepath.Abs(BaseDir)
	if err != nil {
		panic(fmt.Sprintf("failed to resolve absolute path for BaseDir: %v", err))
	}
}

// ParseFile parses a file based on its type and set name
func ParseFile(setName, fileType string) (map[string]interface{}, error) {
	// File path: data/{set_name}/{set_name}.{file_type}
	filePath := filepath.Join(BaseDir, setName, fmt.Sprintf("%s.%s", setName, fileType))

	if _, err := os.Stat(filePath); os.IsNotExist(err) {
		return nil, fmt.Errorf("file %s not found", filePath)
	}

	switch fileType {
	case "txt":
		return parseText(filePath)
	case "xml":
		return parseXML(filePath)
	case "yaml":
		return parseYAML(filePath)
	case "json":
		return parseJSON(filePath)
	case "csv":
		return parseCSV(filePath)
	default:
		return nil, fmt.Errorf("unsupported file type: %s", fileType)
	}
}

func parseText(filePath string) (map[string]interface{}, error) {
	content, err := os.ReadFile(filePath)
	if err != nil {
		return nil, err
	}

	data := make(map[string]interface{})
	lines := strings.Split(string(content), "\n")
	for _, line := range lines {
		if strings.Contains(line, ": ") {
			parts := strings.SplitN(line, ": ", 2)
			data[strings.TrimSpace(parts[0])] = strings.TrimSpace(parts[1])
		}
	}
	return data, nil
}

func parseXML(filePath string) (map[string]interface{}, error) {
	content, err := os.ReadFile(filePath)
	if err != nil {
		return nil, err
	}

	// Define a generic struct to handle XML elements
	type Element struct {
		XMLName xml.Name
		Value   string `xml:",chardata"`
	}

	type Root struct {
		Children []Element `xml:",any"`
	}

	var root Root
	if err := xml.Unmarshal(content, &root); err != nil {
		return nil, err
	}

	data := make(map[string]interface{})
	for _, child := range root.Children {
		data[child.XMLName.Local] = child.Value
	}
	return data, nil
}

func parseYAML(filePath string) (map[string]interface{}, error) {
	data := make(map[string]interface{})
	content, err := os.ReadFile(filePath)
	if err != nil {
		return nil, err
	}

	if err := yaml.Unmarshal(content, &data); err != nil {
		return nil, err
	}
	return data, nil
}

func parseJSON(filePath string) (map[string]interface{}, error) {
	data := make(map[string]interface{})
	content, err := os.ReadFile(filePath)
	if err != nil {
		return nil, err
	}

	if err := json.Unmarshal(content, &data); err != nil {
		return nil, err
	}
	return data, nil
}

func parseCSV(filePath string) (map[string]interface{}, error) {
	data := make(map[string]interface{})
	file, err := os.Open(filePath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	reader := csv.NewReader(file)
	records, err := reader.ReadAll()
	if err != nil {
		return nil, err
	}

	if len(records) < 2 {
		return nil, fmt.Errorf("CSV file must have at least one header row and one data row")
	}

	headers := records[0]
	values := records[1] // Take the first data row only
	if len(values) != len(headers) {
		return nil, fmt.Errorf("row length mismatch in CSV file")
	}
	for i, header := range headers {
		data[header] = values[i]
	}
	return data, nil
}
