/**
 * Custom React hooks for Healthcare AI Assistant
 */

import { useState, useCallback, useRef, useEffect } from 'react';
import { Message, Toast } from '@/lib/types';
import { chatService } from '@/lib/services/api';

/**
 * Hook for managing chat messages
 */
export function useChat(initialPatientId: string = 'p1') {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content:
        'Hello! I am your Healthcare AI Assistant. I can check your symptoms, book an appointment, show your medical summary, or schedule a follow-up. How can I help you today?',
      timestamp: new Date(),
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const patientId = initialPatientId;

  const sendMessage = useCallback(
    async (userMessage: string) => {
      if (!userMessage.trim()) return;

      // Add user message
      const userMsg: Message = {
        id: Date.now().toString(),
        role: 'user',
        content: userMessage,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, userMsg]);
      setIsLoading(true);
      setError(null);

      try {
        const response = await chatService.sendMessage(userMessage, patientId);

        if (response) {
          const assistantMsg: Message = {
            id: (Date.now() + 1).toString(),
            role: 'assistant',
            content: response.reply,
            timestamp: new Date(),
            logs: response.logs,
          };
          setMessages((prev) => [...prev, assistantMsg]);
        } else {
          setError('Failed to get response from AI assistant');
        }
      } catch (err) {
        console.error('Chat error:', err);
        setError('Connection error. Please check your internet connection.');
      } finally {
        setIsLoading(false);
      }
    },
    [patientId]
  );

  const clearMessages = useCallback(() => {
    setMessages([messages[0]]); // Keep initial message
  }, [messages]);

  return {
    messages,
    isLoading,
    error,
    sendMessage,
    clearMessages,
  };
}

/**
 * Hook for managing toast notifications
 */
export function useToast() {
  const [toasts, setToasts] = useState<Toast[]>([]);
  const toastIdRef = useRef(0);

  const addToast = useCallback(
    (
      message: string,
      type: 'success' | 'error' | 'warning' | 'info' = 'info',
      duration: number = 5000
    ) => {
      const id = (toastIdRef.current++).toString();
      const toast: Toast = { id, message, type, duration };

      setToasts((prev) => [...prev, toast]);

      if (duration > 0) {
        setTimeout(() => {
          removeToast(id);
        }, duration);
      }

      return id;
    },
    []
  );

  const removeToast = useCallback((id: string) => {
    setToasts((prev) => prev.filter((toast) => toast.id !== id));
  }, []);

  return {
    toasts,
    addToast,
    removeToast,
  };
}

/**
 * Hook for managing API loading state
 */
export function useAsync<T, E = string>(
  asyncFunction: () => Promise<T>,
  immediate = true
) {
  const [status, setStatus] = useState<
    'idle' | 'pending' | 'success' | 'error'
  >('idle');
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<E | null>(null);

  const execute = useCallback(async () => {
    setStatus('pending');
    setData(null);
    setError(null);

    try {
      const response = await asyncFunction();
      setData(response);
      setStatus('success');
      return response;
    } catch (error) {
      setError(error as E);
      setStatus('error');
      throw error;
    }
  }, [asyncFunction]);

  useEffect(() => {
    if (immediate) {
      execute();
    }
  }, [execute, immediate]);

  return { execute, status, data, error };
}
