"use client";
import { useActions } from "@/utils.jsx/client";
import { EndpointsContext } from "./agent";
import { useState } from "react";
import { HumanMessageText } from "@/components/prebuilt/message";
import {streamResponse} from "@/lib/chat/actions";

export default function Home() {
  const actions = useActions<typeof EndpointsContext>();
  const [elements, setElements] = useState<JSX.Element[]>([]);
  const [components,setComponents] = useState<React.ReactNode>();

  const clicked = async () => {
    const newElements = [...elements];
    const el = await actions.invokeRemoteRunnable();
    console.log(el?.ui);

    newElements.push(
      <div className="flex flex-col w-full gap-1 mt-auto" key={history.length}>
        <HumanMessageText content={"Hello"} />
        <div className="flex flex-col gap-1 w-full max-w-fit mr-auto">
          {el?.ui}
        </div>
      </div>
    );

    setElements(newElements);
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div>
        <button onClick={async() => {setComponents(await streamResponse())}}>Hello</button>
        {/* <button onClick={clicked}>invoke</button>
        <div>{elements}</div> */}
         <div>{components}</div>
      </div>
    </main>
  );
}
