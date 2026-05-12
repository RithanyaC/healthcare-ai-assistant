/**
 * Utility functions for Healthcare AI Assistant
 */

import { Toast } from '@/lib/types';

/**
 * Format a date string to readable format
 */
export function formatDate(dateString: string): string {
  try {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  } catch {
    return dateString;
  }
}

/**
 * Format a datetime string to readable format
 */
export function formatDateTime(dateString: string): string {
  try {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  } catch {
    return dateString;
  }
}

/**
 * Truncate text to specified length
 */
export function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
}

/**
 * Get toast styling based on type
 */
export function getToastStyles(type: Toast['type']): {
  bg: string;
  text: string;
  border: string;
} {
  const styles = {
    success: {
      bg: 'bg-green-50',
      text: 'text-green-800',
      border: 'border-green-200',
    },
    error: {
      bg: 'bg-red-50',
      text: 'text-red-800',
      border: 'border-red-200',
    },
    warning: {
      bg: 'bg-yellow-50',
      text: 'text-yellow-800',
      border: 'border-yellow-200',
    },
    info: {
      bg: 'bg-blue-50',
      text: 'text-blue-800',
      border: 'border-blue-200',
    },
  };

  return styles[type];
}

/**
 * Get risk level styling for triage
 */
export function getRiskLevelStyles(riskLevel: string): {
  bg: string;
  text: string;
  emoji: string;
} {
  const styles = {
    'High': { bg: 'bg-red-100', text: 'text-red-800', emoji: '🔴' },
    'Medium': { bg: 'bg-yellow-100', text: 'text-yellow-800', emoji: '🟡' },
    'Low': { bg: 'bg-green-100', text: 'text-green-800', emoji: '🟢' },
  };

  return styles[riskLevel as keyof typeof styles] || styles['Low'];
}
