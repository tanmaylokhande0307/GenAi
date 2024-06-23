"use client";

import { ReactNode, useContext, createContext } from "react";

const ActionsContext = createContext<any>(null);

export const AIProvider = (props: {
  actions: Record<string, any>;
  children: ReactNode;
}) => {
  return (
    <ActionsContext.Provider value={props.actions}>
      {props.children}
    </ActionsContext.Provider>
  );
};
