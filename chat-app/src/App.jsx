import React, { useEffect, useRef, useState } from "react";
import { ChatBox } from "./components/ChatBox";
import { Box } from "@mui/material";
import { EnterSmsField } from "./components/EnterSMSField";
import "./App.css";
import { addToMessageList } from "./components/chat.reducer";
import { useDispatch, useSelector } from "react-redux";
import { useScrollAnchor } from "./shared/useScrollAnchor";

function App() {
  const messages = useSelector((state) => state.chat.messages);

  const dispatch = useDispatch();

  const { visibilityRef, scrollRef, messagesRef } = useScrollAnchor();

  // WebSocket connection setup goes here

  const sendMessage = () => {
    // Implement sending messages via WebSocket here
  };

  return (
    <Box
      sx={{ display: "flex", flexDirection: "column" }}
      ref={scrollRef}
    >
      <Box sx={{ width: "950px" }} ref={messagesRef}>
        <ChatBox />
        <div
          ref={visibilityRef}
          style={{ height: "1px", width: "100%", backgroundColor: "red" }}
        />
      </Box>
      <Box
        sx={{
          position: "fixed",
          bottom: 0,
          width: "50%",
        }}
      >
        <EnterSmsField />
      </Box>
    </Box>
  );
}

export default App;
