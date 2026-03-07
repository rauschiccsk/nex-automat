/**
 * Standalone Vite config for running renderer in browser (E2E testing).
 * Mirrors renderer config from electron.vite.config.ts.
 */
import { resolve } from 'path'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  root: resolve(__dirname, 'src/renderer'),
  resolve: {
    alias: {
      '@renderer': resolve(__dirname, 'src/renderer/src')
    }
  },
  plugins: [react(), tailwindcss()],
  server: {
    port: 5173,
    host: '0.0.0.0',
  },
  define: {
    // Stub electron-specific globals
    'window.api': 'undefined',
  },
})
