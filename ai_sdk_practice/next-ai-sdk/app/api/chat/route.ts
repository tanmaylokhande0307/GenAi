import { createGoogleGenerativeAI } from "@ai-sdk/google";
import { streamText } from 'ai';
import { PDFLoader } from "langchain/document_loaders/fs/pdf";
import { RecursiveCharacterTextSplitter } from "langchain/text_splitter";
import { FaissStore } from "@langchain/community/vectorstores/faiss";
import { GoogleGenerativeAIEmbeddings } from "@langchain/google-genai";
import { TaskType } from "@google/generative-ai";
import { HNSWLib } from "@langchain/community/vectorstores/hnswlib";


// Allow streaming responses up to 30 seconds
export const maxDuration = 30;


const google = createGoogleGenerativeAI({
    apiKey: "AIzaSyDZhmsfAK3_v9noUhoNjToRBmn0g5HZfM8",
});



export async function POST(req: Request) {
  const { messages } = await req.json();

  const loader = new PDFLoader("/home/debian/source/repos/GenAi/ai_sdk_practice/next-ai-sdk/data/BIM.pdf");
  const docs = await loader.load();

  const splitter = new RecursiveCharacterTextSplitter({
    chunkSize: 1024,
    chunkOverlap: 100,
  });

  const chunks = await splitter.splitDocuments(docs);

  const embeddings = new GoogleGenerativeAIEmbeddings({
    apiKey: "AIzaSyDZhmsfAK3_v9noUhoNjToRBmn0g5HZfM8",
    model: "embedding-001", // 768 dimensions
    taskType: TaskType.RETRIEVAL_DOCUMENT,
    title: "Document title",
  });
  
  
  console.log(chunks[0])  

  const vectorStore = await FaissStore.fromDocuments(
    docs,
    embeddings
  );
  
  const retriever = vectorStore.asRetriever();
  console.log(retriever.invoke("What is the title of the document?"));

  const result = await streamText({
    model: google("models/gemini-1.5-pro-latest"),
    messages,
  });

  return result.toAIStreamResponse();
}
