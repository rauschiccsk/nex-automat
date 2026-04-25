// Grid Formatters - shared formatting functions for all grids

/**
 * Format number as currency (EUR)
 */
export function formatCurrency(value: number | null | undefined, currency = 'EUR'): string {
  if (value == null) return '-';
  return new Intl.NumberFormat('sk-SK', {
    style: 'currency',
    currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(value);
}

/**
 * Format number as percentage
 */
export function formatPercent(value: number | null | undefined, decimals = 1): string {
  if (value == null) return '-';
  return `${value.toFixed(decimals)}%`;
}

/**
 * Format number with decimals
 */
export function formatNumber(value: number | null | undefined, decimals = 2): string {
  if (value == null) return '-';
  return new Intl.NumberFormat('sk-SK', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(value);
}

/**
 * Format integer (no decimals)
 */
export function formatInteger(value: number | null | undefined): string {
  if (value == null) return '-';
  return new Intl.NumberFormat('sk-SK', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value);
}

/**
 * Parse date string that may be in DD.MM.YYYY format
 */
function parseLocalDate(value: string): Date {
  // Try DD.MM.YYYY format first (Slovak/European)
  const ddmmyyyy = value.match(/^(\d{1,2})\.(\d{1,2})\.(\d{4})$/);
  if (ddmmyyyy) {
    const [, day, month, year] = ddmmyyyy;
    return new Date(parseInt(year), parseInt(month) - 1, parseInt(day));
  }
  // Fallback to standard Date parsing (ISO, etc.)
  return new Date(value);
}

/**
 * Format date (Slovak format)
 */
export function formatDate(value: string | Date | null | undefined): string {
  if (value == null) return '-';
  // If already in DD.MM.YYYY format, return as-is
  if (typeof value === 'string' && /^\d{1,2}\.\d{1,2}\.\d{4}$/.test(value)) {
    return value;
  }
  const date = typeof value === 'string' ? parseLocalDate(value) : value;
  if (isNaN(date.getTime())) return '-';
  return date.toLocaleDateString('sk-SK');
}

/**
 * Format datetime (Slovak format)
 */
export function formatDateTime(value: string | Date | null | undefined): string {
  if (value == null) return '-';
  const date = typeof value === 'string' ? parseLocalDate(value) : value;
  if (isNaN(date.getTime())) return '-';
  return date.toLocaleString('sk-SK');
}

/**
 * Format boolean as check/cross
 */
export function formatBoolean(value: boolean | null | undefined): string {
  if (value == null) return '-';
  return value ? '✓' : '✗';
}

/**
 * Truncate text with ellipsis
 */
export function truncateText(value: string | null | undefined, maxLength = 50): string {
  if (value == null) return '-';
  if (value.length <= maxLength) return value;
  return value.substring(0, maxLength - 3) + '...';
}
