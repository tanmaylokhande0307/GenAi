export const socket = new WebSocket("ws://localhost:3001");


export function isSocketReady() {
    return socket.readyState === socket.OPEN;
  }

