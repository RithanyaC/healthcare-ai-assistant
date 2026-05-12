/**
 * Type definitions for Healthcare AI Assistant
 */

// API Response Types
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
  };
}

// Chat Types
export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp?: Date;
  logs?: AgentLog[];
}

export interface AgentLog {
  protocol: string;
  from: string;
  to: string;
  action: string;
  payload: Record<string, any>;
}

export interface ChatResponse {
  reply: string;
  agent: string;
  action?: string;
  data?: Record<string, any>;
  logs?: AgentLog[];
}

// Patient Types
export interface Patient {
  id: string;
  name: string;
  email: string;
  phone?: string;
  age?: number;
  gender?: string;
  medical_history?: string;
  allergies?: string;
  is_active: boolean;
  created_at?: string;
  updated_at?: string;
}

// Doctor Types
export interface Doctor {
  id: string;
  name: string;
  email: string;
  specialization: string;
  available_slots?: string[];
  rating?: number;
}

// Appointment Types
export interface Appointment {
  id: string;
  patient_id: string;
  doctor_id: string;
  slot: string;
  status: 'scheduled' | 'completed' | 'cancelled';
  reason_for_visit?: string;
  created_at?: string;
}

// Medical Record Types
export interface MedicalRecord {
  id: string;
  patient_id: string;
  record_type: 'consultation' | 'lab-test' | 'prescription' | 'follow-up';
  date: string;
  notes?: string;
  diagnosis?: string;
  recommendations?: string;
  created_by?: string;
}

// UI Toast Types
export interface Toast {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  message: string;
  duration?: number;
}
