import { exposeEndpoints } from "@/utils.jsx/server";
import { RemoteRunnable } from "@langchain/core/runnables/remote";
import { HumanMessage } from "@langchain/core/messages";
// import { exposeEndpoints, streamRunnableUI } from "@/utils/server";
import "server-only";
import { Runnable } from "@langchain/core/dist/runnables/base";
import { StreamEvent } from "@langchain/core/dist/tracers/event_stream";
import { createStreamableUI, createStreamableValue } from "ai/rsc";
import { GithubLoading, Github } from "@/components/prebuilt/github";
import { AIMessage } from "@/ai/message";

const API_URL = "http://localhost:8000/chat";

type ToolComponent = {
  loading: (props?: any) => JSX.Element;
  final: (props?: any) => JSX.Element;
};

type ToolComponentMap = {
  [tool: string]: ToolComponent;
};

const TOOL_COMPONENT_MAP: ToolComponentMap = {
  "github-repo": {
    loading: (props?: any) => <GithubLoading {...props} />,
    final: (props?: any) => <Github {...props} />,
  },
};

const invokeRemoteRunnable = async () => {
  "use server";
  const remoteRunnable = new RemoteRunnable({
    url: API_URL,
  });
  const message = new HumanMessage({
    content: "Github repo owner tanmaylokhande0307 repo name GenAi",
  });
  let lastEventValue: StreamEvent | null = null;


  console.log("clicked");
  const ui = createStreamableUI();
  let selectedToolComponent: ToolComponent | null = null;
  let selectedToolUI: ReturnType<typeof createStreamableUI> | null = null;
  const callbacks: Record<
    string,
    ReturnType<typeof createStreamableUI | typeof createStreamableValue>
  > = {};

  for await (const streamEvent of remoteRunnable.streamEvents(
    {
      input: [
        {
          type: "human",
          content: "Github repo owner tanmaylokhande0307 repo name GenAi",
        },
      ],
    },
    {
      version: "v1",
    }
  )) {
    const { output, chunk } = streamEvent.data;
    const [type] = streamEvent.event.split("_").slice(2);
    // console.log("chunk", chunk);
    // console.log("output", output);
    // console.log("type", type);

    const handleInvokeModelEvent = (output: Record<string, any>) => {
      if ("tool_calls" in output && output.tool_calls.length > 0) {
        const toolCall = output.tool_calls[0];
        if (!selectedToolComponent && !selectedToolUI) {
          selectedToolComponent = TOOL_COMPONENT_MAP[toolCall.type];
          selectedToolUI = createStreamableUI(selectedToolComponent.loading());
          ui.append(selectedToolUI?.value);
        }
        console.log("toolCall", toolCall);
      }
    };

    const handleInvokeToolsEvent = (output: Record<string, any>) => {
      console.log("output", output.tool_result);
      if (selectedToolUI && selectedToolComponent) {
        const toolData = output.tool_result;
        selectedToolUI.done(selectedToolComponent.final(toolData));
      }
    };

    const handleChatModelStreamEvent = (
      streamEvent: StreamEvent,
      chunk: Record<string, any>
    ) => {
      if (!callbacks[streamEvent.run_id]) {
        const textStream = createStreamableValue();
        ui.append(<AIMessage value={textStream.value} />);
        callbacks[streamEvent.run_id] = textStream;
      }

      if (callbacks[streamEvent.run_id]) {
        callbacks[streamEvent.run_id].append(chunk.content);
      }
      const textStream = createStreamableValue();
      console.log("textStream", textStream);
      console.log("chunk", chunk.content);
    };

    if (type === "end" && output && typeof output === "object") {
      if (streamEvent.name === "invoke_model") {
        handleInvokeModelEvent(output);
      } else if (streamEvent.name === "invoke_tools") {
        handleInvokeToolsEvent(output);
      }
    }

    if (
      streamEvent.event === "on_chat_model_stream" &&
      chunk &&
      typeof chunk === "object"
    ) {
      handleChatModelStreamEvent(streamEvent, chunk);
    }
    
    lastEventValue = streamEvent;

  }
  ui.done();
  Object.values(callbacks).forEach((cb) => cb.done());
  return { ui: ui.value,lastEventValue };

  // return remoteRunnable.invoke({
  //   input: [message],
  // });
};

export const EndpointsContext = exposeEndpoints({ invokeRemoteRunnable });
