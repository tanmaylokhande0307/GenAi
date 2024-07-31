"use server"
import { exposeEndpoints } from "@/utils/server";
import { RemoteRunnable } from "@langchain/core/runnables/remote";
import { streamText } from "ai";
import { createStreamableValue } from "ai/rsc";

// import { exposeEndpoints, streamRunnableUI } from "@/utils/server";

const API_URL = "http://localhost:8000/response";

export interface Message {
  role: "user" | "assistant";
  content: string;
}

export async function continueConversation() {
  "use server";
  const remoteRunnable = new RemoteRunnable({
    url: API_URL,
  });

  //   const result = await remoteRunnable.stream({
  //     question: "What is transformer",
  //     config: {},
  //     kwargs: {},
  //   });

  //   for await (const chunk of result) {
  //     console.log(chunk);
  //   }

  //   ("use server");
  const stream = createStreamableValue(); 

  (async () => {
    const result = await remoteRunnable.stream({
      question: "What is transformer",
      config: {},
      kwargs: {},
    });

    for await (const chunk of result) {
      console.log(chunk?.response?.content)
      stream.update(chunk?.response?.content);
    }

    stream.done();
  })();

  return {
    newMessage: stream.value,
  };
}
