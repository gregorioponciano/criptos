import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'
import crypto from 'crypto'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const distDir = path.join(__dirname, '../dist')
const statsFile = path.join(__dirname, '../stats.json')

function getFileHash(filePath) {
  const content = fs.readFileSync(filePath)
  return crypto.createHash('sha256').update(content).digest('hex').substring(0, 16)
}

function getDirectorySize(dir) {
  let size = 0
  fs.readdirSync(dir).forEach(file => {
    const filePath = path.join(dir, file)
    const stat = fs.statSync(filePath)
    size += stat.isFile() ? stat.size : getDirectorySize(filePath)
  })
  return size
}

function getFileStats(filePath) {
  const stat = fs.statSync(filePath)
  return {
    name: path.basename(filePath),
    size: stat.size,
    sizeFormatted: (stat.size / 1024).toFixed(2) + ' KB',
    hash: getFileHash(filePath),
    modified: stat.mtime.toISOString()
  }
}

function collectStats() {
  if (!fs.existsSync(distDir)) {
    console.log('⚠️  Pasta dist/ não encontrada. Execute: npm run build')
    return
  }

  console.log('\n╔════════════════════════════════════════════════╗')
  console.log('║        📊 ESTATÍSTICAS DO BUILD 📊             ║')
  console.log('╚════════════════════════════════════════════════╝\n')

  const stats = {
    generated: new Date().toISOString(),
    environment: process.env.NODE_ENV || 'development',
    files: {
      html: [],
      css: [],
      js: []
    },
    totals: {
      files: 0,
      size: 0,
      gzipped: 0
    }
  }

  const assetsDir = path.join(distDir, 'assets')
  if (fs.existsSync(assetsDir)) {
    fs.readdirSync(assetsDir).forEach(file => {
      const filePath = path.join(assetsDir, file)
      const fileStat = getFileStats(filePath)
      
      if (file.endsWith('.html')) stats.files.html.push(fileStat)
      else if (file.endsWith('.css')) stats.files.css.push(fileStat)
      else if (file.endsWith('.js')) stats.files.js.push(fileStat)
      
      stats.totals.size += fileStat.size
      stats.totals.files++
    })
  }

  const indexHtml = path.join(distDir, 'index.html')
  if (fs.existsSync(indexHtml)) {
    stats.files.html.push(getFileStats(indexHtml))
    stats.totals.files++
  }

  console.log('  📦 Arquivos:')
  console.log(`     HTML: ${stats.files.html.length} arquivo(s)`)
  console.log(`     CSS:  ${stats.files.css.length} arquivo(s)`)
  console.log(`     JS:   ${stats.files.js.length} arquivo(s)`)
  
  console.log('\n  📊 Tamanho Total:')
  console.log(`     ${(stats.totals.size / 1024).toFixed(2)} KB`)
  console.log(`     ${(stats.totals.size / 1024 / 1024).toFixed(4)} MB`)
  
  console.log('\n  📋 Detalhes:')
  stats.files.js.forEach(f => {
    console.log(`     JS: ${f.name} (${f.sizeFormatted})`)
  })
  stats.files.css.forEach(f => {
    console.log(`     CSS: ${f.name} (${f.sizeFormatted})`)
  })

  fs.writeFileSync(statsFile, JSON.stringify(stats, null, 2))
  console.log(`\n  ✅ Estatísticas salvas em: stats.json\n`)
}

collectStats()
