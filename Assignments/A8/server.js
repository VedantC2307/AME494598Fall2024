const dotenv = require("dotenv");
dotenv.config();

const https = require('https');
const fs = require('fs');
const express = require('express');
const cors = require('cors');
const errorHandler = require('errorhandler');
const methodOverride = require('method-override');
const WebSocket = require('ws');

const { SERVER_PORT } = process.env;

const app = express();
const port = SERVER_PORT || 4000; // HTTPS typically runs on port 443

// Load the SSL certificate and key
const options = {
    key: fs.readFileSync('key.pem'),
    cert: fs.readFileSync('cert.pem'),
};

app.use(cors());

app.get("/MobileCameraFeed", function (req, res) {
    res.sendFile(__dirname + '/public/index.html');
});

app.use(express.static('public'));
app.use(methodOverride());
app.use(errorHandler());

// Create an HTTPS server
const server = https.createServer(options, app);

// Create a WebSocket server
const wss = new WebSocket.Server({ server });

wss.on('connection', (ws, req) => {
    console.log('WebSocket connection established.');

    let path = req.url.split('/').pop();
    console.log(path);

    ws.on('message', (message) => {
        handleWSMessage(ws, message, path);
    });

    ws.on('close', () => {
        console.log('WebSocket connection closed.');
    });

    ws.on('error', (err) => {
        console.error('WebSocket error: ', err);
    });
});


async function handleWSMessage(ws, message, path) {
    const parsed_data = JSON.parse(message);
    let msg  = {
        "message": parsed_data,
        path
    };
    wss.clients.forEach((client) => {
        if (client !== ws && client.readyState === WebSocket.OPEN) {
            client.send(JSON.stringify(msg));
        }
    });

}

// Start the HTTPS server
server.listen(port, '0.0.0.0',() => {
    console.log(`Server is running over HTTPS on port ${port}/MobileCameraFeed`);
});
