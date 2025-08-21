import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  server: {
    port: 3000,
    host: '0.0.0.0',
    watch: {
      usePolling: true, // Enable polling for Docker
    },
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        // Remove the rewrite - keep the /api prefix
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
  // Configure Vite to use a different temp directory
  cacheDir: '/tmp/vite',
  // Disable the default cache directory
  clearScreen: false,
  // Configure Vite to use a different approach for temporary files
  optimizeDeps: {
    force: true
  },
  // Disable file system caching for development
  experimental: {
    hmrPartialAccept: true
  }
}) 