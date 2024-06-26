"use client";
import Image from "next/image";
import {streamResponse} from "@/lib/chat/actions";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div>
        <button onClick={() => {streamResponse()}}>Hello</button>
      </div>
    </main>
  );
}
