import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'
import crypto from 'crypto'
import zlib from 'zlib'
import { promisify } from 'util'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const distDir = path.join(__dirname, '../dist')
const assetsDir = path.join(distDir, 'assets')

async function compressFile(filePath) {
  const content = fs.readFileSync(filePath)
  const gzip = promisify(zlib.gzip)
  
  const compressed = await gzip(content, { level: 9 })
  const originalSize = content.length
  const compressedSize = compressed.length
  const ratio = ((1 - compressedSize / originalSize) * 100).toFixed(2)
  
  fs.writeFileSync(filePath + '.gz', compressed)
  
  return {
    name: path.basename(filePath),
    original: originalSize,
    compressed: compressedSize,
    ratio: `${ratio}%`
  }
}

async function analyzeFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8')
  const lines = content.split('\n').length
  const chars = content.length
  
  const comments = (content.match(/\/\*[\s\S]*?\*\//g) || []).length
  const strings = (content.match(/['"`][^'"`]*['"`]/g) || []).length
  const functions = (content.match(/function\s+\w+|const\s+\w+\s*=\s*(?:async\s*)?\(|=>\s*{/g) || []).length
  
  return {
    name: path.basename(filePath),
    lines,
    chars,
    comments,
    strings,
    functions,
    complexity: functions > 0 ? Math.round(chars / functions) : 0
  }
}

async function run() {
  if (!fs.existsSync(assetsDir)) {
    console.log('⚠️  Execute: npm run build primeiro')
    return
  }

  console.log('\n╔════════════════════════════════════════════════╗')
  console.log('║       📦 COMPRESSÃO E ANÁLISE 📦               ║')
  console.log('╚════════════════════════════════════════════════╝\n')

  const jsFiles = fs.readdirSync(assetsDir).filter(f => f.endsWith('.js'))
  
  console.log('  📊 Análise de Código:\n')
  for (const file of jsFiles) {
    const analysis = await analyzeFile(path.join(assetsDir, file))
    console.log(`   ${analysis.name}`)
    console.log(`     Linhas: ${analysis.lines} | Caracteres: ${analysis.chars}`)
    console.log(`     Funções: ${analysis.functions} | Complexidade: ${analysis.complexity}`)
    console.log(`     Strings: ${analysis.strings} | Comentários: ${analysis.comments}\n`)
  }

  console.log('  🗜️  Compressão GZIP:\n')
  let totalOriginal = 0
  let totalCompressed = 0
  
  for (const file of jsFiles) {
    const result = await compressFile(path.join(assetsDir, file))
    totalOriginal += result.original
    totalCompressed += result.compressed
    console.log(`   ${result.name}`)
    console.log(`     ${(result.original / 1024).toFixed(2)} KB → ${(result.compressed / 1024).toFixed(2)} KB (${result.ratio})\n`)
  }
  
  const totalSaved = ((1 - totalCompressed / totalOriginal) * 100).toFixed(2)
  console.log('  📈 Resumo:')
  console.log(`     Total original:    ${(totalOriginal / 1024).toFixed(2)} KB`)
  console.log(`     Total comprimido:  ${(totalCompressed / 1024).toFixed(2)} KB`)
  console.log(`     Espaço salvo:      ${totalSaved}%`)
  console.log(`     Economia:           ${((totalOriginal - totalCompressed) / 1024).toFixed(2)} KB\n`)
  
  const hash = crypto.createHash('sha256').update(fs.readdirSync(assetsDir).map(f => 
    fs.readFileSync(path.join(assetsDir, f))
  ).join('')).digest('hex')
  
  console.log(`  🔐 Checksum SHA-256: ${hash}\n`)
}

run()
