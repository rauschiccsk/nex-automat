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
 * Format date (Slovak format)
 */
export function formatDate(value: string | Date | null | undefined): string {
  if (value == null) return '-';
  const date = typeof value === 'string' ? new Date(value) : value;
  if (isNaN(date.getTime())) return '-';
  return date.toLocaleDateString('sk-SK');
}

/**
 * Format datetime (Slovak format)
 */
export function formatDateTime(value: string | Date | null | undefined): string {
  if (value == null) return '-';
  const date = typeof value === 'string' ? new Date(value) : value;
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
