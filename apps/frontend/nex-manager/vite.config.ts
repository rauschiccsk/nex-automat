import { resolve } from 'path'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  resolve: {
    alias: {
      '@renderer': resolve(__dirname, 'src'),
      '@': resolve(__dirname, 'src')
    }
  },
  plugins: [
    react(),
    tailwindcss(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['icon.svg'],
      manifest: {
        name: 'NEX Manager',
        short_name: 'NEX Manager',
        description: 'NEX Automat module manager',
        theme_color: '#0f172a',
        background_color: '#ffffff',
        display: 'standalone',
        start_url: '/',
        scope: '/',
        lang: 'sk',
        icons: [
          {
            src: 'icon.svg',
            sizes: 'any',
            type: 'image/svg+xml',
            purpose: 'any maskable'
          }
        ]
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,svg,woff2}'],
        runtimeCaching: [
          {
            // Module registry — relatively stable, OK to cache briefly
            urlPattern: /^https?:\/\/[^/]+\/api\/system\/modules/,
            handler: 'NetworkFirst',
            options: {
              cacheName: 'nex-system-modules',
              networkTimeoutSeconds: 5,
              expiration: { maxEntries: 10, maxAgeSeconds: 300 } // 5 min
            }
          }
          // Conservative: NO caching of /api/users, /api/pab, /api/eshop, /api/migration —
          // those have frequently mutated data. Browser uses normal HTTP cache only.
          // /api/auth/* is never cached (security).
        ],
        navigateFallback: '/index.html',
        navigateFallbackDenylist: [/^\/api/]
      }
    })
  ],
  server: {
    port: 5173,
    host: '0.0.0.0'
  },
  build: {
    outDir: 'dist',
    sourcemap: true
  }
})
