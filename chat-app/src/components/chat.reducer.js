import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";

const initialState = {
  messages: [
    {
      text: "Hello how can I help you",
      isReceived: true,
    },
    
  ],
};

export const chatSlice = createSlice({
  name: "chat",
  initialState,
  reducers: {
    addToMessageList: (state, action) => {
      return {
        ...state,
        messages: [...state.messages, action.payload],
      };
    },
  },
  extraReducers: (builder) => {
    // builder.addCase(fetchInitialQuestions.fulfilled, (state, action) => {
    //   const regex = /{([^{}]+)}/;
    //   const match = action.payload.match(regex);
    //   let question = "";
    //   let category = "";
    //   if (match) {
    //     const extractedJsonString = match[1];
    //     console.log("extractedJsonString ", extractedJsonString);
    //     const extractedJsonObject = JSON.parse("{" + extractedJsonString + "}");
    //     console.log("extractedJsonObject ", extractedJsonObject);
    //     question = extractedJsonObject.question;
    //     category = extractedJsonObject.category;
    //     console.log("category: ", category);
    //   } else {
    //     console.log("No JSON found between {} signs.");
    //   }
    //   const messageObject = {
    //     text: question,
    //     isReceived: true,
    //   };
    //   console.log("classified_risk_category set: ", category);
    //   return {
    //     ...state,
    //     messages: [...state.messages, messageObject],
    //     classified_risk_category: category,
    //   };
    // });
    // builder.addCase(fetchInitialQuestions.rejected, (state, action) => {
    //   console.log("rejected fetchInitialQuestions", action.payload);
    //   return { ...state };
    // });
  },
});

export const { addToMessageList } = chatSlice.actions;
export default chatSlice.reducer;
