import { Annotation } from "@langchain/langgraph";
import { BaseMessage } from "@langchain/core/messages";

const AgentState = Annotation.Root({
  messages: Annotation<BaseMessage[]>({
    reducer: (x, y) => x.concat(y),
  }),
});

const mess:any = ["hello"]
const mess1:any = ["bye"]

console.log(AgentState.State.messages.push(mess,mess1))