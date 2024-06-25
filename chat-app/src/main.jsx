import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import "./index.css";
import { Provider } from "react-redux";
import { store } from "./store/store.js";
import { WebSocketConnector } from "./WebSocketConnector.jsx";

ReactDOM.createRoot(document.getElementById("root")).render(
  <Provider store={store}>
    <WebSocketConnector />
    <App />
  </Provider>
);
