import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const packageJson = path.join(__dirname, '../package.json')
const changelog = path.join(__dirname, '../CHANGELOG.md')
const versionFile = path.join(__dirname, '../version.json')

function getVersion() {
  if (fs.existsSync(versionFile)) {
    return JSON.parse(fs.readFileSync(versionFile, 'utf-8'))
  }
  return {
    major: 1,
    minor: 0,
    patch: 0,
    build: 1,
    date: new Date().toISOString(),
    hash: Date.now().toString(36).toUpperCase()
  }
}

function saveVersion(version) {
  version.date = new Date().toISOString()
  version.hash = Date.now().toString(36).toUpperCase()
  fs.writeFileSync(versionFile, JSON.stringify(version, null, 2))
  
  const pkg = JSON.parse(fs.readFileSync(packageJson, 'utf-8'))
  pkg.version = `${version.major}.${version.minor}.${version.patch}`
  fs.writeFileSync(packageJson, JSON.stringify(pkg, null, 2))
}

function updateChangelog(version, type) {
  const date = new Date().toLocaleDateString('pt-BR')
  const time = new Date().toLocaleTimeString('pt-BR')
  const versionStr = `${version.major}.${version.minor}.${version.patch}`
  
  const entry = `## [${versionStr}] - ${date} ${time} [${type.toUpperCase()}]\n\n`
  
  let content = ''
  if (fs.existsSync(changelog)) {
    content = fs.readFileSync(changelog, 'utf-8')
  }
  
  content = `# Changelog\n\n${entry}${content}`
  fs.writeFileSync(changelog, content)
}

function bump(type) {
  let version = getVersion()
  const oldVersion = `${version.major}.${version.minor}.${version.patch}`
  
  switch(type) {
    case 'major':
      version.major++
      version.minor = 0
      version.patch = 0
      break
    case 'minor':
      version.minor++
      version.patch = 0
      break
    case 'patch':
      version.patch++
      break
    default:
      console.log('❌ Tipo inválido. Use: major, minor ou patch')
      return
  }
  
  saveVersion(version)
  updateChangelog(version, type)
  
  console.log(`\n✅ Versão atualizada!`)
  console.log(`   ${oldVersion} → ${version.major}.${version.minor}.${version.patch}`)
  console.log(`   Build: ${version.build}`)
  console.log(`   Hash: ${version.hash}\n`)
}

function check() {
  const version = getVersion()
  const pkg = JSON.parse(fs.readFileSync(packageJson, 'utf-8'))
  
  console.log('\n╔════════════════════════════════════════════════╗')
  console.log('║         📋 INFORMAÇÕES DA VERSÃO 📋            ║')
  console.log('╚════════════════════════════════════════════════╝\n')
  console.log(`   Versão: ${pkg.version}`)
  console.log(`   Major:  ${version.major}`)
  console.log(`   Minor:  ${version.minor}`)
  console.log(`   Patch:  ${version.patch}`)
  console.log(`   Build:  ${version.build}`)
  console.log(`   Hash:   ${version.hash}`)
  console.log(`   Data:   ${new Date(version.date).toLocaleString('pt-BR')}\n`)
}

const command = process.argv[2]

if (command === 'bump') {
  bump(process.argv[3] || 'patch')
} else if (command === 'check') {
  check()
} else {
  console.log('\n📌 Comandos disponíveis:')
  console.log('   npm run version:bump major  # Nova versão maior')
  console.log('   npm run version:bump minor  # Nova versão menor')
  console.log('   npm run version:bump patch  # Correção de bug')
  console.log('   npm run version:check       # Ver versão atual\n')
}
