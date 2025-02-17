"use client";

import { useActions } from "@/utils/client";
import { useChat } from "ai/react";
import { EndpointsContext } from "./agent";

import { exposeEndpoints } from "@/utils/server";
import { RemoteRunnable } from "@langchain/core/runnables/remote";
import { streamText } from "ai";
import { useState } from "react";
import { continueConversation, Message } from "./actions";
import { readStreamableValue } from "ai/rsc";

// import { exposeEndpoints, streamRunnableUI } from "@/utils/server";
// import "server-only";

const API_URL = "http://localhost:8000/response";

inputs: {
  input: string;
  chat_history: [role: string, content: string][];
  file?: {
    base64: string;
    extension: string;
  };
}
const remoteRunnable = new RemoteRunnable({
  url: API_URL,
});

export default function Chat() {
  const [mes, setMes] = useState("");
  const [conversation, setConversation] = useState<Message[]>([]);

  const actions = useActions<typeof EndpointsContext>();

  const handleButtonClick = async () => {
    // const result = await remoteRunnable.stream({
    //   question: "What is transformer",
    //   config: {},
    //   kwargs: {},
    // });

    // for await (const chunk of result  ) {
    //   setMes(o => o.concat(chunk?.response?.content))
    //   console.log(chunk?.response?.content);
    // }

    // await actions.agent()

    const { newMessage } = await continueConversation();

    let textContent = "";

    for await (const delta of readStreamableValue(newMessage)) {
      textContent = `${textContent}${delta}`;
      console.log(delta)

      setConversation([
        { role: "assistant", content: textContent },
      ]);
    }
  };
  // const { messages, input, handleInputChange, handleSubmit } = useChat();
  return (
    <div className="flex flex-col w-full max-w-md py-24 mx-auto">
      {/* {messages.map((m) => (
        <div key={m.id}>
          {m.role === "user" ? "User: " : "AI: "}
          {m.content}
        </div>
      ))} */}

      {/* {mes} */}
      <div>
        {conversation.map((message, index) => (
          <div key={index}>
            {message.role}: {message.content}
          </div>
        ))}
      </div>

      <button onClick={handleButtonClick}>Start</button>
      {/* <form onSubmit={handleSubmit}>
        <input
          className="fixed bottom-0 w-full max-w-md p-2 mb-8 border border-gray-300 rounded shadow-xl"
          value={input}
          placeholder="Say something..."
          onChange={handleInputChange}
        />
      </form> */}
    </div>  
  );
}
