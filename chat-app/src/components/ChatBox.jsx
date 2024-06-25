import {
  Box,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
} from "@mui/material";
import { MessageFooter } from "./MessageFooter";
import { useSelector } from "react-redux";

const msgBgSx = {
  padding: "10px",
  paddingLeft: "20px",
  paddingRight: "20px",
  borderRadius: "10px",
  width: "unset",
  minWidth: 100,
  maxWidth: "80%",
  justifyContent: "space-between",
  flexWrap: "wrap",
};

export const ChatBox = () => {
  const messages = useSelector((state) => state.chat.messages);
  return (
    <List
      sx={{
        display: "grid",
        maxWidth: "100%",
        gap: "10px",
        padding: "10px",
        // height: "450px",
      }}
    >
      {messages?.map((data, index) => {
        return (
          <ListItem
            // ref={index === userSMS.length - 1 ? scrollRef : null}
            key={`msg-${index}`}
            style={{
              justifySelf: data.isReceived ? "flex-start" : "flex-end",
              backgroundColor: data.isReceived ? "#0000" : "	#ffa700",
              border: data.isReceived ? `1px solid #6C737F` : 0,
              ...msgBgSx,
            }}
          >
            {data.text}
            <MessageFooter />
          </ListItem>
        );
      })}
    </List>
  );
};
