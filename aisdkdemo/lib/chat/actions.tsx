'use server';
import { streamText } from "ai";
import { createGoogleGenerativeAI } from "@ai-sdk/google";
import { GoogleGenerativeAI } from "@google/generative-ai";
import { streamUI } from 'ai/rsc';
import { z } from "zod";

const LoadingComponent = () => (
  <div className="animate-pulse p-4">getting weather...</div>
);

const getWeather = async (location: string) => {
  await new Promise((resolve) => setTimeout(resolve, 2000));
  return "82°F️ ☀️";
};

interface WeatherProps {
  location: string;
  weather: string;
}

const WeatherComponent = (props: WeatherProps) => (
  <div className="border border-neutral-200 p-4 rounded-lg max-w-fit">
    The weather in {props.location} is {props.weather}
  </div>
);

const genAI = new GoogleGenerativeAI(
  process.env.GOOGLE_GENERATIVE_AI_API_KEY || ""
);

const google = createGoogleGenerativeAI({
  apiKey: "apikey",
});

export const streamResponse = async () => {
  const result = await streamUI({
    model: google("models/gemini-pro"),
    prompt: "Get the weather for San Francisco",
    // text: ({ content }) => <div>content {content}</div>,
    tools: {
      getWeather: {
        description: "Get the weather for a location",
        parameters: z.object({
          location: z.string(),
        }),
        generate: async function* ({ location }) {
          yield <LoadingComponent />;
          const weather = await getWeather(location);
          return <WeatherComponent weather={weather} location={location} />;
        },
      },
    },
  });

  return result.value;
};

// export const streamResponse = async () => {
//   (async () => {
//     const { textStream } = await streamText({
//       model: google("models/gemini-pro"),
//       prompt: "Invent a new holiday and describe its traditions.",
//     });

//     for await (const textPart of textStream) {
//       console.log(textPart);
//     }
//   })();
// };
