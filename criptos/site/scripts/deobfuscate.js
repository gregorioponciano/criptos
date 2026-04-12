import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const distDir = path.join(__dirname, '../dist/assets')

console.log('⚠️  AVISO: Desofuscação é apenas para debugging!')
console.log('🔓 Restaurando arquivos em:', distDir)
console.log('❌ Desofuscação automática não é possível.')
console.log('📝 Use ferramentas como:', 'https://lelinhtinh.github.io/de4js/')
