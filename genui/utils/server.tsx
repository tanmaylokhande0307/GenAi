import "server-only";

import { ReactNode, isValidElement } from "react";
import { AIProvider } from "./client";
import {
  CallbackManagerForToolRun,
  CallbackManagerForRetrieverRun,
  CallbackManagerForChainRun,
} from "@langchain/core/callbacks/manager";
// import { createStreamableUI, createStreamableValue } from "ai/rsc";
import { Runnable, RunnableLambda } from "@langchain/core/runnables";
import { CompiledStateGraph } from "@langchain/langgraph";
import { StreamEvent } from "@langchain/core/tracers/log_stream";
// import { AIMessage } from "@/ai/message";

const STREAM_UI_RUN_NAME = "stream_runnable_ui";

export function exposeEndpoints <T extends Record<string,unknown>> (actions:T,):{
    (props: {children: ReactNode}): Promise<JSX.Element>;
    $$types?: T;
}{
    return async function AI(props: {children: ReactNode}) {
        return <AIProvider actions={actions}>
            {props.children}
        </AIProvider>   
    }
}

export function withResolvers<T>() {
  let resolve!: (value: T) => void;
  let reject!: (reason?: any) => void;

  const innerPromise = new Promise<T>((res, rej) => {
    resolve = res;
    reject = rej;
  });

  return [innerPromise,resolve,reject] as const
}

