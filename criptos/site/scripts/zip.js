import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'
import crypto from 'crypto'
import archiver from 'archiver'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const distDir = path.join(__dirname, '../dist')
const outputDir = path.join(__dirname, '../releases')

function createManifest() {
  const pkg = JSON.parse(fs.readFileSync(path.join(__dirname, '../package.json'), 'utf-8'))
  const files = []
  
  function walkDir(dir, base = '') {
    if (!fs.existsSync(dir)) return
    fs.readdirSync(dir).forEach(file => {
      const filePath = path.join(dir, file)
      const relativePath = path.join(base, file)
      const stat = fs.statSync(filePath)
      
      if (stat.isDirectory()) {
        walkDir(filePath, relativePath)
      } else {
        files.push({
          name: relativePath,
          size: stat.size,
          hash: crypto.createHash('sha256').update(fs.readFileSync(filePath)).digest('hex').substring(0, 16)
        })
      }
    })
  }
  
  walkDir(distDir)
  
  const manifest = {
    version: pkg.version,
    build: Date.now(),
    buildDate: new Date().toISOString(),
    environment: process.env.NODE_ENV || 'production',
    files: files,
    totals: {
      files: files.length,
      size: files.reduce((acc, f) => acc + f.size, 0)
    }
  }
  
  return manifest
}

function createZip(manifest) {
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true })
  }
  
  const version = manifest.version
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-').split('T')[0]
  const zipName = `release-${version}-${timestamp}.zip`
  const zipPath = path.join(outputDir, zipName)
  
  const output = fs.createWriteStream(zipPath)
  const archive = archiver('zip', { zlib: { level: 9 } })
  
  output.on('close', () => {
    console.log('\n╔════════════════════════════════════════════════╗')
    console.log('║       📦 PACOTE DE RELEASE CRIADO 📦           ║')
    console.log('╚════════════════════════════════════════════════╝\n')
    console.log(`   📁 Arquivo: ${zipName}`)
    console.log(`   📊 Tamanho: ${(archive.pointer() / 1024 / 1024).toFixed(2)} MB`)
    console.log(`   📦 Arquivos: ${manifest.totals.files}`)
    console.log(`   💾 Compactado: ${((1 - archive.pointer() / manifest.totals.size) * 100).toFixed(2)}%\n`)
  })
  
  archive.pipe(output)
  archive.directory(distDir, false)
  archive.finalize()
  
  fs.writeFileSync(path.join(outputDir, `manifest-${version}.json`), JSON.stringify(manifest, null, 2))
  fs.writeFileSync(path.join(outputDir, `RELEASE-${version}.md`), `# Release ${version}\n\nData: ${manifest.buildDate}\n\n## Arquivos\n\n${manifest.files.map(f => `- ${f.name} (${(f.size/1024).toFixed(2)} KB)`).join('\n')}\n\n## Checksums\n\n${manifest.files.map(f => `- ${f.hash}  ${f.name}`).join('\n')}\n`)
}

console.log('\n╔════════════════════════════════════════════════╗')
console.log('║       📦 CRIANDO PACOTE DE RELEASE 📦          ║')
console.log('╚════════════════════════════════════════════════╝\n')

console.log('  📋 Gerando manifest...')
const manifest = createManifest()
console.log(`  ✅ ${manifest.totals.files} arquivos catalogados`)

console.log('  🗜️  Criando ZIP...')
createZip(manifest)
