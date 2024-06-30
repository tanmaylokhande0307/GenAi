import { exposeEndpoints } from "@/utils/server";
import { RemoteRunnable } from "@langchain/core/runnables/remote";
// import { exposeEndpoints, streamRunnableUI } from "@/utils/server";
import "server-only";

const API_URL = "http://localhost:8000/chat";

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

  for await (const streamEvent of remoteRunnable.streamEvents("What is BIM", {
    version: "v1",
  })) {
    const { output, chunk } = streamEvent.data;
    // const [type] = streamEvent.event.split("_").slice(2);
    const type = streamEvent.event;

    // console.log("streamEvent", streamEvent);

    if (type === "end" && output && typeof output === "object") {
      if (streamEvent.name === "invoke_model") {
        // handleInvokeModelEvent(output);
        console.log("output", output);
      } else if (streamEvent.name === "invoke_tools") {
        // handleInvokeToolsEvent(output);
        console.log(output);
      }
    }

    // if (type === "on_chain_stream") {
    //   console.log(chunk);
    // }

    if (type === "on_llm_stream") {
      console.log(chunk);
    }
    // if (type === "on_parser_stream") {
    //   console.log(chunk);
    // }

    if (
      streamEvent.event === "on_chat_model_stream" &&
      chunk &&
      typeof chunk === "object"
    ) {
      //   handleChatModelStreamEvent(streamEvent, chunk);
      console.log("chunk", chunk);
      console.log("streamevent", streamEvent);
    }
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
