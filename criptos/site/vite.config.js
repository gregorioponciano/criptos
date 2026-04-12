import { defineConfig } from 'vite'

export default defineConfig({
  root: 'src',
  base: './',
  server: {
    port: 5173,
    open: true
  },
  build: {
    outDir: '../dist',
    emptyOutDir: true
  }
})
