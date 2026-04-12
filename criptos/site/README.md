# 🔐 Sistema de Criptografia e Build

Sistema completo de desenvolvimento, build e ofuscação para projetos web.

---

## 🚀 Quick Start

```bash
npm install              # Instalar dependências
npm run dev              # Iniciar desenvolvimento
npm run build:prod       # Build de produção
```

---

## 📋 Scripts Disponíveis

### Desenvolvimento
```bash
npm run dev              # Servidor de desenvolvimento (localhost:5173)
npm run preview          # Testar build localmente
npm run preview:dist     # Servir pasta dist/ (npm install -g serve)
```

### Build
```bash
npm run build            # Build padrão
npm run build:dev        # Build ambiente dev
npm run build:staging    # Build ambiente staging
npm run build:prod       # Build ambiente produção
npm run build:obfuscate  # Build + ofuscação completa
npm run build:all        # Build + ofuscação + estatísticas
```

### Ofuscação
```bash
npm run obfuscate        # Ofuscar JS no dist/ (nível padrão)
npm run obfuscate -- --medium   # Nível médio de ofuscação
npm run obfuscate -- --high     # Nível máximo de ofuscação
```

### Compressão e Análise
```bash
npm run compress         # Comprimir arquivos com GZIP
npm run analyze          # Análise detalhada do código
npm run stats            # Estatísticas do build
npm run report           # Relatório completo de build
```

### Versionamento
```bash
npm run version:check    # Ver versão atual
npm run version:bump major   # Nova versão maior
npm run version:bump minor   # Nova versão menor
npm run version:bump patch   # Correção de bug
```

### Limpeza
```bash
npm run clean            # Limpar pasta dist/
npm run clean:all        # Limpar dist/ + cache Vite
```

### Deploy
```bash
./deploy.sh dev          # Deploy ambiente dev
./deploy.sh staging      # Deploy ambiente staging
./deploy.sh prod         # Deploy produção
./deploy.sh --clean      # Deploy com limpeza
./deploy.sh --rollback   # Rollback última versão
```

---

## 🏗️ Estrutura do Projeto

```
projeto/
├── src/                    # Código fonte
│   ├── assets/            # Imagens, fontes, etc
│   ├── css/              # Estilos
│   └── js/               # JavaScript
├── dist/                  # Build de produção
├── scripts/               # Scripts de automação
│   ├── obfuscate.js      # Ofuscação de código
│   ├── compress.js        # Compressão GZIP
│   ├── stats.js          # Estatísticas
│   ├── version.js        # Versionamento
│   ├── report.js         # Relatórios
│   └── zip.js            # Criar release
├── logs/                  # Logs de build
├── releases/              # Pacotes de release
├── public/                # Arquivos públicos
├── package.json
├── vite.config.js
└── .gitignore
```

---

## 🔒 Níveis de Ofuscação

### Standard (padrão)
- Compactação básica
- Controles de fluxo
- String arrays em base64
- Renomeação hexadecimal

### Medium
- Tudo do standard +
- Dead code injection
- Proteção DevTools
- Encoding RC4
- Renomeação de globals

### High
- Tudo do medium +
- Controles de fluxo máximo
- String array 100%
- Bloqueio de domínio
- Anti-debug avançado

---

## 📊 Fluxo de Build

```
┌─────────┐     ┌─────────┐     ┌─────────────┐     ┌──────────┐
│   src/  │────▶│  vite   │────▶│    dist/    │────▶│ ofuscado │
└─────────┘     │  build  │     │   (minified) │     └──────────┘
                └─────────┘     └─────────────┘
                      │
                      ▼
                ┌─────────────┐
                │  compress   │
                │   (gzip)    │
                └─────────────┘
```

---

## 🛡️ Recursos de Segurança

- **Obfuscação de código**: Variaveis renomeadas
- **String arrays**: Strings em arrays codificados
- **Dead code injection**: Código falso adicionado
- **Controle de fluxo**: Código embaralhado
- **Proteção DevTools**: Bloqueio de console
- **Self-defending**: Proteção contra modificação
- **Unicode escape**: Caracteres especiais

---

## 📦 Versionamento Semântico

```
major.minor.patch
│     │     └── Correções
│     └─────── Novas funcionalidades
└────────────── Mudanças incompatíveis
```

---

## 🔧 Configuração de Ambientes

```javascript
// vite.config.js
export default defineConfig({
  root: 'src',
  server: {
    port: 5173,
    open: true
  },
  build: {
    outDir: '../dist',
    sourcemap: false // desabilitar em prod
  }
})
```

---

## 📝 Logs e Monitoramento

```bash
# Ver logs de build
cat logs/build-2024-01-15.log

# Ver estatísticas
cat stats.json

# Ver relatório
npm run report
```

---

## 🌐 Deploy

Configure as credenciais no `deploy.sh`:

```bash
DEPLOY_USER="seu_usuario"
DEPLOY_HOST="seu_servidor.com"
DEPLOY_PATH="/var/www/projeto"
```

---

## 📌 Checklist de Produção

- [ ] `npm run build:prod` executou sem erros
- [ ] Ofuscação aplicada (`npm run obfuscate`)
- [ ] Estatísticas verificadas (`npm run stats`)
- [ ] Versão atualizada (`npm run version:bump patch`)
- [ ] Release criado (`npm run zip`)
- [ ] Deploy realizado (`./deploy.sh prod`)
- [ ] Health check verificado
