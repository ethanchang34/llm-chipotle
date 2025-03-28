'use client';

import { useState } from 'react';

export default function Home() {
  // const [input, setInput] = useState('')
  const [messages, setMessages] = useState<string[]>([]);
  const [listening, setListening] = useState(false);

  const handleListen = () => {
    const es = new EventSource("http://localhost:8000/transcribe");
    setListening(true);

    es.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.text) {
        setMessages((prev) => [...prev, `🗣️ ${data.text}`]);
      }
      if (data.reply) {
        setMessages((prev) => [...prev, `🤖 ${data.reply}`]);
      }
    };

    es.onerror = () => {
      es.close();
      setListening(false);
    };
  };
  // const sendMessage = async () => {
  //   if (!input.trim()) return

  //   setMessages(prev => [...prev, `🧑 ${input}`])

  //   const res = await fetch('http://localhost:8000/chat', {
  //     method: 'POST',
  //     headers: { 'Content-Type': 'application/json' },
  //     body: JSON.stringify({ message: input }),
  //   })

  //   const data = await res.json()
  //   setMessages(prev => [...prev, `🤖 ${data.reply}`])
  //   setInput('')
  // }

  return (
    // <main style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
    //   <h1>🌯 Chipotle Chatbot</h1>
    //   <div style={{ marginBottom: '1rem' }}>
    //     {messages.map((msg, i) => (
    //       <div key={i}>{msg}</div>
    //     ))}
    //   </div>
    //   <input
    //     value={input}
    //     onChange={e => setInput(e.target.value)}
    //     onKeyDown={e => e.key === 'Enter' && sendMessage()}
    //     placeholder="Say something..."
    //     style={{ width: '300px', padding: '0.5rem' }}
    //   />
    //   <button onClick={sendMessage} style={{ marginLeft: '1rem' }}>Send</button>
    // </main>
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
          <li key={idx} className="bg-gray-100 p-2 rounded text-black whitespace-pre-wrap">
            {m}
          </li>
        ))}
      </ul>
    </main>
  );
}
