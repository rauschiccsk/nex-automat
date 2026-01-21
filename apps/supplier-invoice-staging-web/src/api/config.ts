import apiClient from './client';

/**
 * Staging Web Configuration
 * Controls which features are available based on customer settings
 */
export interface StagingConfig {
  customer_name: string;
  allow_price_edit: boolean;
  allow_margin_edit: boolean;
  allow_approve: boolean;
  allow_reject: boolean;
  show_nex_columns: boolean;
}

// Default config (used if API fails)
const DEFAULT_CONFIG: StagingConfig = {
  customer_name: 'Unknown',
  allow_price_edit: false,
  allow_margin_edit: false,
  allow_approve: true,
  allow_reject: true,
  show_nex_columns: true,
};

// Cached config
let cachedConfig: StagingConfig | null = null;

/**
 * Get staging configuration from backend
 * Caches the result for subsequent calls
 */
export async function getStagingConfig(): Promise<StagingConfig> {
  if (cachedConfig) {
    return cachedConfig;
  }

  try {
    const response = await apiClient.get<StagingConfig>('/staging/config');
    cachedConfig = response.data;
    console.log('[Config] Loaded staging config:', cachedConfig);
    return cachedConfig;
  } catch (error) {
    console.warn('[Config] Failed to load config, using defaults:', error);
    return DEFAULT_CONFIG;
  }
}

/**
 * Clear cached config (for testing/refresh)
 */
export function clearConfigCache(): void {
  cachedConfig = null;
}
