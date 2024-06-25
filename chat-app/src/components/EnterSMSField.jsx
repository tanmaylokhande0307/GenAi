import { IconButton, InputAdornment, TextField } from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { addToMessageList } from "./chat.reducer";
import { socket } from "../socket";

export function EnterSmsField() {
  const messages = useSelector((state) => state.chat.messages);
  const [input, setInput] = useState("");
  const dispatch = useDispatch();
  const handleChange = (e) => {
    setInput(e.target.value);
  };
  const handleSubmit = () => {
    const payload = { text: input, isReceived: false };
    socket.send(JSON.stringify(payload));
    dispatch(addToMessageList(payload));
    setInput("");
  };

  return (
    <TextField
      sx={{
        backgroundColor: "#fffee0",
      }}
      fullWidth
      InputProps={{
        endAdornment: (
          <IconButton onClick={handleSubmit}>
            <InputAdornment>
              <SendIcon />
            </InputAdornment>
          </IconButton>
        ),
      }}
      onChange={handleChange}
      value={input}
      placeholder="Enter your query"
    ></TextField>
  );
}
