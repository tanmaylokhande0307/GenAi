
import { configureStore } from "@reduxjs/toolkit";
import chatReducer from "../components/chat.reducer";

export const store = configureStore({
  reducer: {
    chat: chatReducer,
  },
});
