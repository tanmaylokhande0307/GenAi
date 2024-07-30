import { exposeEndpoints } from "@/utils/server";
import { RemoteRunnable } from "@langchain/core/runnables/remote";
import { streamText } from "ai";

// import { exposeEndpoints, streamRunnableUI } from "@/utils/server";
import "server-only";

const API_URL = "http://localhost:8000/response";

export async function agent() {
  // inputs: {
  //   input: string;
  //   chat_history: [role: string, content: string][];
  //   file?: {
  //     base64: string;
  //     extension: string;
  //   };
  // }
  "use server";
  const remoteRunnable = new RemoteRunnable({
    url: API_URL,
  });

  const result = await remoteRunnable.stream({
    question: "What is transformer",
    config: {},
    kwargs: {},
  });

  for await (const chunk of result  ) {
    console.log(chunk);
  }
  
  
  // const stream = await remoteRunnable.invoke({
  //   input: "What is BIM",
  // });

  // console.log(stream);

  // for await (const chunk of stream) {
  //   console.log(chunk);
  // }

  //   return streamRunnableUI(remoteRunnable, {
  //     input: [
  //       ...inputs.chat_history.map(([role, content]) => ({
  //         type: role,
  //         content,
  //       })),
  //       {
  //         type: "human",
  //         content: inputs.input,
  //       },
  //     ],
  //   });
}

export const EndpointsContext = exposeEndpoints({ agent });
