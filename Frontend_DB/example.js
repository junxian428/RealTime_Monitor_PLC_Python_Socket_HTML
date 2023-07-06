const WebSocket = require('websocket').w3cwebsocket;

const client = new WebSocket('ws://localhost:8005/');

client.onopen = () => {
    console.log('WebSocket client connected');
};

client.onmessage = (message) => {
    console.log('Received message from server:', message.data);
};

client.onclose = () => {
    console.log('WebSocket connection closed');
};
