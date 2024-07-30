'use client';

import { useActions } from '@/utils/client';
import { useChat } from 'ai/react';
import { EndpointsContext } from './agent';

import { exposeEndpoints } from "@/utils/server";
import { RemoteRunnable } from "@langchain/core/runnables/remote";
import { streamText } from "ai";
import { useState } from 'react';

// import { exposeEndpoints, streamRunnableUI } from "@/utils/server";
// import "server-only";

const API_URL = "http://localhost:8000/response";

  // inputs: {
  //   input: string;
  //   chat_history: [role: string, content: string][];
  //   file?: {
  //     base64: string;
  //     extension: string;
  //   };
  // }
  const remoteRunnable = new RemoteRunnable({
    url: API_URL,
  });

  

export default function Chat() {

  const [mes,setMes] = useState("")


  const actions = useActions<typeof EndpointsContext>();

  const handleButtonClick = async() => {
    // "use server"
    const result = await remoteRunnable.stream({
      question: "What is transformer",
      config: {},
      kwargs: {},
    });
  
    for await (const chunk of result  ) {
      setMes(o => o.concat(chunk?.response?.content))
      console.log(chunk?.response?.content);
    }
  
    // await actions.agent()
  }
  const { messages, input, handleInputChange, handleSubmit } = useChat();
  return (
    <div className="flex flex-col w-full max-w-md py-24 mx-auto">
      {messages.map(m => (
        <div key={m.id}>
          {m.role === 'user' ? 'User: ' : 'AI: '}
          {m.content}
        </div>
      ))}

      {mes}

      <button onClick={handleButtonClick}>Start</button>
      <form onSubmit={handleSubmit}>
        <input
          className="fixed bottom-0 w-full max-w-md p-2 mb-8 border border-gray-300 rounded shadow-xl"
          value={input}
          placeholder="Say something..."
          onChange={handleInputChange}
        />
      </form>
    </div>
  );
}