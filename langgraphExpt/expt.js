"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var langgraph_1 = require("@langchain/langgraph");
var AgentState = langgraph_1.Annotation.Root({
    messages: (0, langgraph_1.Annotation)({
        reducer: function (x, y) { return x.concat(y); },
    }),
});
var mess = ["hello"];
var mess1 = ["bye"];
console.log(AgentState.spec.messages);
