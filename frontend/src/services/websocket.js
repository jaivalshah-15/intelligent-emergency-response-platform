export function connectWebSocket(onMessage) {
  const socket = new WebSocket(
    "ws://localhost:8000/api/ws"
  );

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    onMessage(data);
  };

  socket.onerror = (error) => {
    console.error(
      "WebSocket error:",
      error
    );
  };

  return socket;
}