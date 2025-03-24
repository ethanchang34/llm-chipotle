'use client'

import { useState } from 'react'

export default function Home() {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState<string[]>([])

  const sendMessage = async () => {
    if (!input.trim()) return

    setMessages(prev => [...prev, `🧑 ${input}`])

    const res = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: input }),
    })

    const data = await res.json()
    setMessages(prev => [...prev, `🤖 ${data.reply}`])
    setInput('')
  }

  return (
    <main style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>🌯 Chipotle Chatbot</h1>
      <div style={{ marginBottom: '1rem' }}>
        {messages.map((msg, i) => (
          <div key={i}>{msg}</div>
        ))}
      </div>
      <input
        value={input}
        onChange={e => setInput(e.target.value)}
        onKeyDown={e => e.key === 'Enter' && sendMessage()}
        placeholder="Say something..."
        style={{ width: '300px', padding: '0.5rem' }}
      />
      <button onClick={sendMessage} style={{ marginLeft: '1rem' }}>Send</button>
    </main>
  )
}
