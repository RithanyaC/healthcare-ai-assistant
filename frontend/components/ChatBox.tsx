"use client";

import { useState, useRef, useEffect } from "react";
import { useChat, useToast } from "@/lib/hooks";
import { Message } from "@/lib/types";
import { LoadingSpinner, ToastNotification } from "./ui/Components";

/**
 * ChatBox Component
 * Main chat interface for healthcare AI assistant
 */
export default function ChatBox() {
  const { messages, isLoading, error, sendMessage } = useChat("p1");
  const [input, setInput] = useState("");
  const { toasts, addToast, removeToast } = useToast();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto scroll
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  useEffect(() => {
    if (error) {
      addToast(error, "error");
    }
  }, [error, addToast]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!input.trim() || isLoading) return;

    const userInput = input;
    setInput("");

    await sendMessage(userInput);
  };

  return (
    <div className="flex flex-col h-full w-full bg-gradient-to-br from-slate-900 to-slate-950">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-thin scrollbar-thumb-slate-700 scrollbar-track-transparent">
        {messages.map((msg) => (
          <ChatMessage key={msg.id} message={msg} />
        ))}

        {isLoading && (
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-slate-700 flex items-center justify-center">
              <LoadingSpinner />
            </div>

            <div className="bg-slate-800 border border-slate-700 rounded-2xl rounded-tl-sm p-4">
              <p className="text-slate-400 text-sm">
                Thinking...
              </p>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Toasts */}
      <div className="fixed bottom-20 right-4 space-y-2 z-50">
        {toasts.map((toast) => (
          <ToastNotification
            key={toast.id}
            message={toast.message}
            type={toast.type}
            onClose={() => removeToast(toast.id)}
          />
        ))}
      </div>

      {/* Input */}
      <div className="border-t border-slate-700 bg-slate-900 p-6">
        <form onSubmit={handleSubmit} className="flex gap-4">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Tell me about your symptoms..."
            disabled={isLoading}
            className="flex-1 bg-slate-800 border border-slate-600 rounded-full px-6 py-3 text-white placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition disabled:opacity-50"
          />

          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="bg-blue-600 hover:bg-blue-700 text-white rounded-full px-6 py-3 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? <LoadingSpinner /> : "Send"}
          </button>
        </form>
      </div>
    </div>
  );
}

/**
 * Chat Message
 */
function ChatMessage({ message }: { message: Message }) {
  const isUser = message.role === "user";

  return (
    <div
      className={`flex flex-col ${
        isUser ? "items-end" : "items-start"
      }`}
    >
      <div
        className={`max-w-[80%] p-4 rounded-2xl ${
          isUser
            ? "bg-blue-600 text-white rounded-tr-sm"
            : "bg-slate-800 text-slate-200 rounded-tl-sm border border-slate-700"
        }`}
      >
        <p className="leading-relaxed whitespace-pre-wrap break-words">
          {message.content}
        </p>
      </div>

      {/* Agent Logs */}
      {message.logs && message.logs.length > 0 && (
        <details className="mt-2 text-xs text-slate-400 w-full max-w-[80%]">
          <summary className="cursor-pointer hover:text-slate-300">
            Show agent logs ({message.logs.length})
          </summary>

          <div className="mt-2 space-y-1 bg-slate-900 rounded p-2 border border-slate-700">
            {message.logs.map((log, idx) => (
              <div
                key={idx}
                className="font-mono text-slate-500"
              >
                <strong>{log.from}</strong> →{" "}
                <strong>{log.to}</strong>: {log.action}
              </div>
            ))}
          </div>
        </details>
      )}
    </div>
  );
}
