import "server-only";
import { ReactNode } from "react";
import { AIProvider } from "./client";

export function exposeEndpoints<T extends Record<string, unknown>>(
    actions: T,
  ): {
    (props: { children: ReactNode }): Promise<JSX.Element>;
    $$types?: T;
  } {
    return async function AI(props: { children: ReactNode }) {
      return <AIProvider actions={actions}>{props.children}</AIProvider>;
    };
  }