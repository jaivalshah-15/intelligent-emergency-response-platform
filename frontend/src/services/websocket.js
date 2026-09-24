export function connectWebSocket(onMessage) {
  const apiUrl = import.meta.env.VITE_API_URL;

  const wsUrl = apiUrl
    .replace(/^https:/, "wss:")
    .replace(/^http:/, "ws:");

  const socket = new WebSocket(`${wsUrl}/api/ws`);

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    onMessage(data);
  };

  socket.onerror = (error) => {
    console.error("WebSocket error:", error);
  };

  return socket;
}
