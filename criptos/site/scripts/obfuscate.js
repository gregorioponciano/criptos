import JavaScriptObfuscator from 'javascript-obfuscator'
import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const distDir = path.join(__dirname, '../dist/assets')

const CONFIG = {
  level: process.argv.includes('--high') ? 'high' : 
          process.argv.includes('--medium') ? 'medium' : 'standard',
  
  levels: {
    standard: {
      compact: true,
      controlFlowFlattening: true,
      controlFlowFlatteningThreshold: 0.5,
      deadCodeInjection: false,
      debugProtection: false,
      disableConsoleOutput: false,
      identifierNamesGenerator: 'hexadecimal',
      numbersToExpressions: true,
      renameGlobals: false,
      selfDefending: true,
      shuffleStringArray: true,
      splitStrings: true,
      splitStringsChunkLength: 5,
      stringArray: true,
      stringArrayCallsTransform: true,
      stringArrayCallsTransformThreshold: 0.5,
      stringArrayEncoding: ['base64'],
      stringArrayIndexShift: true,
      stringArrayRotate: true,
      stringArrayShuffle: true,
      stringArrayThreshold: 0.5,
      transformObjectKeys: false,
      unicodeEscapeSequence: true
    },
    medium: {
      compact: true,
      controlFlowFlattening: true,
      controlFlowFlatteningThreshold: 0.75,
      deadCodeInjection: true,
      deadCodeInjectionThreshold: 0.3,
      debugProtection: true,
      debugProtectionInterval: 2000,
      disableConsoleOutput: true,
      identifierNamesGenerator: 'hexadecimal',
      numbersToExpressions: true,
      renameGlobals: true,
      selfDefending: true,
      shuffleStringArray: true,
      splitStrings: true,
      splitStringsChunkLength: 3,
      stringArray: true,
      stringArrayCallsTransform: true,
      stringArrayCallsTransformThreshold: 0.75,
      stringArrayEncoding: ['base64', 'rc4'],
      stringArrayIndexShift: true,
      stringArrayRotate: true,
      stringArrayShuffle: true,
      stringArrayThreshold: 0.75,
      transformObjectKeys: true,
      unicodeEscapeSequence: true
    },
    high: {
      compact: true,
      controlFlowFlattening: true,
      controlFlowFlatteningThreshold: 1,
      deadCodeInjection: true,
      deadCodeInjectionThreshold: 0.5,
      debugProtection: true,
      debugProtectionInterval: 2000,
      disableConsoleOutput: true,
      domainLock: [],
      identifierNamesGenerator: 'hexadecimal',
      numbersToExpressions: true,
      renameGlobals: true,
      selfDefending: true,
      shuffleStringArray: true,
      splitStrings: true,
      splitStringsChunkLength: 2,
      stringArray: true,
      stringArrayCallsTransform: true,
      stringArrayCallsTransformThreshold: 1,
      stringArrayEncoding: ['rc4'],
      stringArrayIndexShift: true,
      stringArrayRotate: true,
      stringArrayShuffle: true,
      stringArrayThreshold: 1,
      transformObjectKeys: true,
      unicodeEscapeSequence: true
    }
  }
}

function obfuscateFile(filePath) {
  const code = fs.readFileSync(filePath, 'utf-8')
  const obfuscated = JavaScriptObfuscator.obfuscate(code, CONFIG.levels[CONFIG.level])
  fs.writeFileSync(filePath, obfuscated.getObfuscatedCode())
  
  const originalSize = Buffer.byteLength(code, 'utf-8')
  const obfuscatedSize = Buffer.byteLength(obfuscated.getObfuscatedCode(), 'utf-8')
  const reduction = ((originalSize - obfuscatedSize) / originalSize * 100).toFixed(2)
  
  console.log(`  🔒 ${path.basename(filePath)}`)
  console.log(`     ${(originalSize / 1024).toFixed(2)} KB → ${(obfuscatedSize / 1024).toFixed(2)} KB (${reduction}%)`)
}

function processDirectory(dir) {
  if (!fs.existsSync(dir)) {
    console.log('  ⚠️  Pasta dist/ não encontrada. Execute: npm run build')
    return
  }
  
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.js'))
  console.log(`\n  📁 Processando ${files.length} arquivo(s)...\n`)
  
  files.forEach(file => {
    obfuscateFile(path.join(dir, file))
  })
}

console.log('\n╔════════════════════════════════════════════════╗')
console.log('║     🔐 SISTEMA DE OFUSCAÇÃO DE CÓDIGO 🔐       ║')
console.log('╠════════════════════════════════════════════════╣')
console.log(`║  Nível: ${CONFIG.level.toUpperCase().padEnd(36)}║`)
console.log('╚════════════════════════════════════════════════╝')
console.log('\n🔒 Iniciando obfuscação...')

processDirectory(distDir)

console.log('\n✅ Processo concluído!')
console.log('📂 Arquivos obcados em: dist/assets/\n')
