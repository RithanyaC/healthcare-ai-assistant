/**
 * API Service Layer
 * Handles all communication with backend and MCP server
 */

import { ApiResponse, ChatResponse, Message } from '@/lib/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const MCP_URL = process.env.NEXT_PUBLIC_MCP_URL || 'http://localhost:8001';

/**
 * Generic fetch wrapper with error handling
 */
async function apiRequest<T>(
  url: string,
  options: RequestInit = {}
): Promise<ApiResponse<T>> {
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }

    const data = await response.json();
    return data as ApiResponse<T>;
  } catch (error) {
    console.error('API Request Error:', error);
    return {
      success: false,
      error: {
        code: 'REQUEST_FAILED',
        message: error instanceof Error ? error.message : 'Unknown error',
      },
    };
  }
}

/**
 * Chat Service
 */
export const chatService = {
  /**
   * Send a message to the chat orchestrator
   */
  async sendMessage(
    message: string,
    patientId: string = 'p1'
  ): Promise<ChatResponse | null> {
    const response = await apiRequest<ChatResponse>(
      `${API_BASE_URL}/api/chat`,
      {
        method: 'POST',
        body: JSON.stringify({
          message,
          patient_id: patientId,
        }),
      }
    );

    return response.success ? response.data || null : null;
  },
};

/**
 * Patient Service
 */
export const patientService = {
  /**
   * Get patient summary with records and appointments
   */
  async getSummary(patientId: string) {
    return apiRequest(`${API_BASE_URL}/api/patients/${patientId}/summary`);
  },

  /**
   * Get patient details
   */
  async getPatient(patientId: string) {
    return apiRequest(`${API_BASE_URL}/api/patients/${patientId}`);
  },

  /**
   * Get patient medical records
   */
  async getRecords(patientId: string, recordType?: string) {
    const query = new URLSearchParams();
    if (recordType) query.append('record_type', recordType);
    return apiRequest(
      `${API_BASE_URL}/api/patients/${patientId}/records?${query}`
    );
  },
};

/**
 * Appointment Service
 */
export const appointmentService = {
  /**
   * Find available appointment slots
   */
  async findSlots(specialization: string) {
    return apiRequest(
      `${API_BASE_URL}/api/slots?specialization=${specialization}`
    );
  },

  /**
   * Book an appointment
   */
  async bookAppointment(
    patientId: string,
    doctorId: string,
    slot: string
  ) {
    return apiRequest(`${API_BASE_URL}/api/appointments`, {
      method: 'POST',
      body: JSON.stringify({
        patient_id: patientId,
        doctor_id: doctorId,
        slot,
      }),
    });
  },

  /**
   * Get patient appointments
   */
  async getAppointments(patientId: string) {
    return apiRequest(`${API_BASE_URL}/api/appointments/${patientId}`);
  },
};

/**
 * Medical Records Service
 */
export const medicalService = {
  /**
   * Create a follow-up record
   */
  async createFollowup(patientId: string, notes: string) {
    return apiRequest(`${API_BASE_URL}/api/followups`, {
      method: 'POST',
      body: JSON.stringify({
        patient_id: patientId,
        notes,
      }),
    });
  },

  /**
   * Create a medical record
   */
  async createRecord(
    patientId: string,
    recordType: string,
    notes: string,
    diagnosis?: string
  ) {
    return apiRequest(`${API_BASE_URL}/api/patients/${patientId}/records`, {
      method: 'POST',
      body: JSON.stringify({
        record_type: recordType,
        notes,
        diagnosis,
      }),
    });
  },
};

/**
 * Health Check Service
 */
export const healthService = {
  /**
   * Check backend health
   */
  async checkBackend() {
    return apiRequest(`${API_BASE_URL}/api/health`);
  },

  /**
   * Check MCP server health
   */
  async checkMCP() {
    return apiRequest(`${MCP_URL}/health`);
  },
};
