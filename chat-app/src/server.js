import { server as WebSocketServer } from 'websocket';
import http from 'http';

// Create an HTTP server
const server = http.createServer((request, response) => {
    response.writeHead(404);
    response.end();
});

server.listen(3001, () => {
    console.log((new Date()) + ' Server is listening on port 8080');
});

// Create a WebSocket server
const wsServer = new WebSocketServer({
    httpServer: server
});

// Keep track of all connected clients
const clients = [];

wsServer.on('request', (request) => {
    const connection = request.accept(null, request.origin);
    clients.push(connection);
    console.log((new Date()) + ' Connection accepted.');

    connection.on('message', (message) => {
        if (message.type === 'utf8') {
            console.log('Received Message: ' + message.utf8Data);

            // Send a response back to the client
            // connection.sendUTF('Hello from server!');

            // Broadcast the message to all connected clients
            broadcast(message.utf8Data);
        }
    });

    connection.on('close', (reasonCode, description) => {
        console.log((new Date()) + ' Peer ' + connection.remoteAddress + ' disconnected.');
        // Remove the client from the list of connected clients
        clients.splice(clients.indexOf(connection), 1);
    });
});

// Function to broadcast messages to all connected clients
function broadcast(message) {
    clients.forEach((client) => {
        client.sendUTF(message);
    });
}

// Function to send a message to a specific client
function sendToClient(client, message) {
    client.sendUTF(message);
}
