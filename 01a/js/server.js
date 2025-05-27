const express = require('express');
const { parseFile } = require('./parser');
const swaggerUi = require('swagger-ui-express');
const swaggerJsdoc = require('swagger-jsdoc');

const app = express();
const port = 3000;


const swaggerOptions = {
    definition: {
        openapi: '3.0.0',
        info: {
            title: 'Data Parsing Server (JavaScript)',
            version: '1.0.0',
            description: 'A JavaScript/Express server to parse data files in multiple formats.'
        },
        servers: [
            {
                url: 'http://localhost:3000',
                description: 'Local server'
            }
        ]
    },
    apis: ['./server.js']
};

const swaggerDocs = swaggerJsdoc(swaggerOptions);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocs));


const SETS = ['books', 'movies'];
const FILE_TYPES = ['txt', 'xml', 'yaml', 'json', 'csv'];

/**
 * @swagger
 * /:
 *   get:
 *     summary: Welcome message
 *     tags: [General]
 *     responses:
 *       200:
 *         description: A welcome message with available sets and formats
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 message:
 *                   type: string
 *                 available_sets:
 *                   type: array
 *                   items:
 *                     type: string
 *                 available_formats:
 *                   type: array
 *                   items:
 *                     type: string
 */
app.get('/', (req, res) => {
    res.json({
        message: 'Welcome to the Data Parsing Server (JavaScript)!',
        available_sets: SETS,
        available_formats: FILE_TYPES
    });
});

/**
 * @swagger
 * /parse/{setName}/{fileType}:
 *   get:
 *     summary: Parse a specific file from a set
 *     tags: [Parsing]
 *     parameters:
 *       - in: path
 *         name: setName
 *         required: true
 *         schema:
 *           type: string
 *         description: The name of the set (e.g., 'books' or 'movies')
 *       - in: path
 *         name: fileType
 *         required: true
 *         schema:
 *           type: string
 *         description: The file format (e.g., 'txt', 'xml', 'yaml', 'json', 'csv')
 *     responses:
 *       200:
 *         description: The parsed data
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 set:
 *                   type: string
 *                 format:
 *                   type: string
 *                 data:
 *                   type: object
 *       400:
 *         description: Invalid set name or file type
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 error:
 *                   type: string
 *       404:
 *         description: File not found
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 error:
 *                   type: string
 *       500:
 *         description: Error parsing file
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 error:
 *                   type: string
 */
app.get('/parse/:setName/:fileType', async (req, res) => {
    const { setName, fileType } = req.params;

    // Validate setName
    if (!SETS.includes(setName)) {
        return res.status(400).json({ error: `Invalid set name. Available sets: ${SETS}` });
    }

    // Validate fileType
    if (!FILE_TYPES.includes(fileType)) {
        return res.status(400).json({ error: `Invalid file type. Available types: ${FILE_TYPES}` });
    }

    try {
        const data = await parseFile(setName, fileType);
        res.json({
            set: setName,
            format: fileType,
            data
        });
    } catch (error) {
        if (error.message.includes('not found')) {
            res.status(404).json({ error: error.message });
        } else {
            res.status(500).json({ error: `Error parsing file: ${error.message}` });
        }
    }
});

/**
 * @swagger
 * /parse/{setName}:
 *   get:
 *     summary: Parse all files in a set
 *     tags: [Parsing]
 *     parameters:
 *       - in: path
 *         name: setName
 *         required: true
 *         schema:
 *           type: string
 *         description: The name of the set (e.g., 'books' or 'movies')
 *     responses:
 *       200:
 *         description: The parsed data for all file types
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 set:
 *                   type: string
 *                 data:
 *                   type: object
 *                   additionalProperties:
 *                     type: object
 *       400:
 *         description: Invalid set name
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 error:
 *                   type: string
 */
app.get('/parse/:setName', async (req, res) => {
    const { setName } = req.params;

    if (!SETS.includes(setName)) {
        return res.status(400).json({ error: `Invalid set name. Available sets: ${SETS}` });
    }

    const result = {};
    for (const fileType of FILE_TYPES) {
        try {
            const data = await parseFile(setName, fileType);
            result[fileType] = data;
        } catch (error) {
            result[fileType] = { error: error.message };
        }
    }

    res.json({
        set: setName,
        data: result
    });
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
    console.log(`Swagger UI available at http://localhost:${port}/api-docs`);
});