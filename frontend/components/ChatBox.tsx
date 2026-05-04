"use client";

import { useState, useRef, useEffect } from 'react';

type AgentLog = {
  protocol: string;
  from: string;
  to: string;
  action: string;
  payload: any;
};

type Message = {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  logs?: AgentLog[];
};

export default function ChatBox() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: 'Hello! I am your Healthcare AI Assistant. I can check your symptoms, book an appointment, show your medical summary, or schedule a follow-up. How can I help you today?',
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage.content, patient_id: "p1" }), // Demo uses p1
      });

      const data = await response.json();
      
      if (data.success) {
        setMessages(prev => [...prev, {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: data.data.reply,
          logs: data.data.logs
        }]);
      } else {
        setMessages(prev => [...prev, {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: "Sorry, I encountered an error: " + (data.error?.message || "Unknown error"),
        }]);
      }
    } catch (error) {
      setMessages(prev => [...prev, {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: "Sorry, I couldn't reach the server. Make sure the backend is running.",
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full w-full">
      <div className="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-thin scrollbar-thumb-slate-700 scrollbar-track-transparent">
        {messages.map((msg) => (
          <div key={msg.id} className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
            <div 
              className={`max-w-[80%] p-4 rounded-2xl ${
                msg.role === 'user' 
                  ? 'bg-blue-600 text-white rounded-tr-sm' 
                  : 'bg-slate-800 text-slate-200 rounded-tl-sm border border-slate-700'
              }`}
            >
              <p className="whitespace-pre-wrap">{msg.content}</p>
            </div>
            
            {/* Agent Logs Display */}
            {msg.logs && msg.logs.length > 0 && (
              <div className="max-w-[80%] mt-2 flex flex-col gap-2">
                {msg.logs.map((log, idx) => (
                  <div key={idx} className="text-xs bg-slate-900/80 p-3 rounded-lg border border-slate-700 font-mono text-slate-400">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-purple-400 font-semibold">{log.from}</span>
                      <span className="text-slate-500">→</span>
                      <span className="text-blue-400 font-semibold">{log.to}</span>
                    </div>
                    <div className="text-green-400 mb-1">Action: {log.action}</div>
                    <div className="text-slate-500 truncate">
                      Payload: {JSON.stringify(log.payload)}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
        {isLoading && (
          <div className="flex items-start">
            <div className="bg-slate-800 p-4 rounded-2xl rounded-tl-sm border border-slate-700 flex items-center gap-2">
              <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
              <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
              <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-4 bg-slate-900 border-t border-slate-800">
        <form onSubmit={handleSubmit} className="flex gap-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your symptoms, ask for a summary, or book an appointment..."
            className="flex-1 bg-slate-800 border border-slate-700 text-white rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
            disabled={isLoading}
          />
          <button 
            type="submit" 
            disabled={isLoading || !input.trim()}
            className="bg-blue-600 hover:bg-blue-500 disabled:bg-slate-700 disabled:text-slate-400 text-white px-6 py-3 rounded-xl font-medium transition-all"
          >
            Send
          </button>
        </form>
      </div>
    </div>
  );
}
