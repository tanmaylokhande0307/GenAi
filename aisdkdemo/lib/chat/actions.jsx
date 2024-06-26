import { streamText } from "ai";
import { createGoogleGenerativeAI } from "@ai-sdk/google";
import { GoogleGenerativeAI } from "@google/generative-ai";

const genAI = new GoogleGenerativeAI(
  process.env.GOOGLE_GENERATIVE_AI_API_KEY || ""
);

const google = createGoogleGenerativeAI({
  apiKey: "apikey",
});

export const streamResponse = async () => {
  (async () => {
    const { textStream } = await streamText({
      model: google("models/gemini-pro"),
      prompt: "Invent a new holiday and describe its traditions.",
    });

    for await (const textPart of textStream) {
      console.log(textPart);
    }
  })();
};
