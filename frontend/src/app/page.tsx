'use client';

import { constants } from 'buffer';
import { useState } from 'react';

export default function Home() {
  const [messages, setMessages] = useState<string[]>(['']);
  const [listening, setListening] = useState(false);

  const handleListen = () => {
    const es = new EventSource("http://localhost:8000/transcribe");
    setListening(true);

    es.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.text && data.complete == false) {
        // Replace the last message with updated incomplete text
        setMessages((prev) => {
          const updated = [...prev];
          updated[updated.length-1] = `🗣️ ${data.text}`;
          return updated;
        });
      }

      if (data.text && data.complete === true) {
        // Finalize the last placeholder, then add a new blank message
        setMessages((prev) => {
          const updated = [...prev];
          updated[updated.length - 1] = `🗣️ ${data.text}`;
          return [...updated, ''];
        });
      }

      if (data.reply) {
        // Finalize the last placeholder, then add a new blank message
        setMessages((prev) => {
          const updated = [...prev];
          updated[updated.length - 1] = `🤖 ${data.reply}`;
          return [...updated, ''];
        });
      }
    };

    es.onerror = () => {
      es.close();
      setListening(false);
    };
  };


  return (
    <main className="p-6">
      <h1 className="text-xl font-bold mb-4">🎙️ Chipotle Voice Order</h1>
      <button
        onClick={handleListen}
        className="px-4 py-2 bg-green-600 text-white rounded"
        disabled={listening}
      >
        {listening ? "🎧 Listening..." : "🎤 Start Voice Order"}
      </button>

      <ul className="mt-6 space-y-2">
        {messages.map((m, idx) => (
          <li
            key={idx}
            className={`p-2 rounded whitespace-pre-wrap ${
              m.startsWith('🗣️') ? 'bg-gray-100 text-black' :
              m.startsWith('🤖') ? 'bg-green-100 text-black' : 'text-gray-400'
            }`}
          >
            {m}
          </li>
        ))}
      </ul>
    </main>
  );
}
