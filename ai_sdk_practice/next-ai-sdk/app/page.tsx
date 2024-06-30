'use client';

import { useActions } from '@/utils/client';
import { useChat } from 'ai/react';
import { EndpointsContext } from './agent';

export default function Chat() {
  const actions = useActions<typeof EndpointsContext>();

  const handleButtonClick = async() => {
    await actions.agent()
  }
  const { messages, input, handleInputChange, handleSubmit } = useChat();
  return (
    <div className="flex flex-col w-full max-w-md py-24 mx-auto">
      {messages.map(m => (
        <div key={m.id}>
          {m.role === 'user' ? 'User: ' : 'AI: '}
          {m.content}
        </div>
      ))}

      <button onClick={handleButtonClick}>Start</button>
      <form onSubmit={handleSubmit}>
        <input
          className="fixed bottom-0 w-full max-w-md p-2 mb-8 border border-gray-300 rounded shadow-xl"
          value={input}
          placeholder="Say something..."
          onChange={handleInputChange}
        />
      </form>
    </div>
  );
}