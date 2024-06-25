import { useDispatch } from "react-redux";
import { socket } from "./socket";
import { addToMessageList } from "./components/chat.reducer";
import { useEffect } from "react";

export const WebSocketConnector = () => {
  const dispatch = useDispatch();


  socket.onmessage = (event) => {
    try {
      const receivedMessage = JSON.parse(event.data);
      const payload = { text: receivedMessage, isReceived: true };
      dispatch(addToMessageList(payload));
    } catch (error) {
      console.log("Parsing failed:", error);
    }
  };

  const connect = () => {
    console.log("Initiating websocket connection");
  };

  const disconnect = () => {
    console.log("Closing websocket connection");
    socket.close();
  };

  useEffect(() => {
    connect();

    return () => {
      disconnect();
    };
  }, []);

  return <></>;
};
