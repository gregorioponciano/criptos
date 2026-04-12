import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const rootDir = path.join(__dirname, '..')

function log(message, type = 'info') {
  const icons = {
    info: 'ℹ️',
    success: '✅',
    warning: '⚠️',
    error: '❌',
    start: '🚀',
    end: '🏁'
  }
  
  const timestamp = new Date().toLocaleTimeString('pt-BR')
  console.log(`${icons[type]} [${timestamp}] ${message}`)
}

function getBuildInfo() {
  const pkg = JSON.parse(fs.readFileSync(path.join(rootDir, 'package.json'), 'utf-8'))
  const versionFile = path.join(rootDir, 'version.json')
  
  let version = { major: 0, minor: 0, patch: 0, build: 0 }
  if (fs.existsSync(versionFile)) {
    version = JSON.parse(fs.readFileSync(versionFile, 'utf-8'))
  }
  
  return {
    name: pkg.name,
    version: `${version.major}.${version.minor}.${version.patch}`,
    build: version.build,
    hash: version.hash,
    date: version.date
  }
}

function createBuildLog(buildInfo, step, status) {
  const logDir = path.join(rootDir, 'logs')
  if (!fs.existsSync(logDir)) {
    fs.mkdirSync(logDir, { recursive: true })
  }
  
  const date = new Date().toISOString().split('T')[0]
  const logFile = path.join(logDir, `build-${date}.log`)
  
  const entry = `[${new Date().toISOString()}] [${buildInfo.version}] [Build #${buildInfo.build}] ${step}: ${status}\n`
  
  fs.appendFileSync(logFile, entry)
}

function analyzeBuild() {
  const distDir = path.join(rootDir, 'dist')
  const assetsDir = path.join(distDir, 'assets')
  
  if (!fs.existsSync(assetsDir)) {
    return null
  }
  
  const stats = {
    files: {
      html: 0,
      css: 0,
      js: 0,
      images: 0
    },
    totalSize: 0,
    byType: {}
  }
  
  function analyzeDir(dir) {
    fs.readdirSync(dir).forEach(file => {
      const filePath = path.join(dir, file)
      const stat = fs.statSync(filePath)
      
      if (stat.isDirectory()) {
        analyzeDir(filePath)
      } else {
        const ext = path.extname(file).toLowerCase()
        stats.totalSize += stat.size
        
        if (ext === '.html') stats.files.html++
        else if (ext === '.css') stats.files.css++
        else if (ext === '.js') stats.files.js++
        else if (['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'].includes(ext)) {
          stats.files.images++
        }
        
        if (!stats.byType[ext]) stats.byType[ext] = { count: 0, size: 0 }
        stats.byType[ext].count++
        stats.byType[ext].size += stat.size
      }
    })
  }
  
  analyzeDir(distDir)
  return stats
}

function printReport(buildInfo, stats) {
  console.log('\n╔════════════════════════════════════════════════╗')
  console.log('║        📊 RELATÓRIO DE BUILD 📊                 ║')
  console.log('╚════════════════════════════════════════════════╝\n')
  
  console.log('  🏗️  Informações do Build:')
  console.log(`     Projeto:    ${buildInfo.name}`)
  console.log(`     Versão:     ${buildInfo.version}`)
  console.log(`     Build:      #${buildInfo.build}`)
  console.log(`     Hash:       ${buildInfo.hash}`)
  console.log(`     Data:       ${new Date(buildInfo.date).toLocaleString('pt-BR')}`)
  
  if (stats) {
    console.log('\n  📦 Arquivos Gerados:')
    console.log(`     HTML:       ${stats.files.html} arquivo(s)`)
    console.log(`     CSS:        ${stats.files.css} arquivo(s)`)
    console.log(`     JS:         ${stats.files.js} arquivo(s)`)
    console.log(`     Imagens:    ${stats.files.images} arquivo(s)`)
    
    console.log('\n  💾 Tamanho Total:')
    console.log(`     ${(stats.totalSize / 1024).toFixed(2)} KB`)
    console.log(`     ${(stats.totalSize / 1024 / 1024).toFixed(4)} MB`)
    
    console.log('\n  📋 Por Tipo:')
    Object.entries(stats.byType).forEach(([ext, data]) => {
      console.log(`     ${ext.padEnd(6)}: ${data.count} arquivo(s) - ${(data.size/1024).toFixed(2)} KB`)
    })
  }
  
  console.log('\n')
}

function generateReport() {
  const buildInfo = getBuildInfo()
  const stats = analyzeBuild()
  
  log('Gerando relatório de build...', 'start')
  printReport(buildInfo, stats)
  log('Relatório gerado com sucesso!', 'success')
}

generateReport()
