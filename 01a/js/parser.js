// 01a/js/parser.js
const fs = require('fs').promises;
const path = require('path');
const yaml = require('js-yaml');
const xml2js = require('xml2js');

// Base directory for files (relative to project root, which is Mandatory_1/)
const BASE_DIR = path.resolve(__dirname, '..', '..'); // Move up two directories to Mandatory_1/

async function parseText(filePath) {
    const content = await fs.readFile(filePath, 'utf8');
    const data = {};
    data ['content'] = content.split('\n').map(line => line.trim());
    return data;
}

async function parseXml(filePath) {
    const content = await fs.readFile(filePath, 'utf8');
    const parser = new xml2js.Parser();
    const result = await parser.parseStringPromise(content);
    const rootKey = Object.keys(result)[0];
    const data = {};
    for (const [key, value] of Object.entries(result[rootKey])) {
        data[key] = value[0];
    }
    return data;
}

async function parseYaml(filePath) {
    const content = await fs.readFile(filePath, 'utf8');
    return yaml.load(content);
}

async function parseJson(filePath) {
    const content = await fs.readFile(filePath, 'utf8');
    return JSON.parse(content);
}

async function parseCsv(filePath) {
    const content = await fs.readFile(filePath, 'utf8');
    const lines = content.split('\n');
    const headers = lines[0].split(',');
    const values = lines[1].split(',');
    const data = {};
    for (let i = 0; i < headers.length; i++) {
        data[headers[i].trim()] = values[i].trim();
    }
    return data;
}

async function parseFile(setName, fileType) {
    const filePath = path.join(BASE_DIR, 'data', setName, `${setName}.${fileType}`);
    
    try {
        await fs.access(filePath);
    } catch (error) {
        throw new Error(`File ${filePath} not found`);
    }

    switch (fileType) {
        case 'txt':
            return parseText(filePath);
        case 'xml':
            return parseXml(filePath);
        case 'yaml':
            return parseYaml(filePath);
        case 'json':
            return parseJson(filePath);
        case 'csv':
            return parseCsv(filePath);
        default:
            throw new Error(`Unsupported file type: ${fileType}`);
    }
}

module.exports = { parseFile };