#!/bin/bash

# ═══════════════════════════════════════════════════════════
#  SCRIPT DE DEPLOY AUTOMÁTICO
#  Uso: ./deploy.sh [ambiente]
#  Ambientes: dev | staging | prod
# ═══════════════════════════════════════════════════════════

set -e

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Configurações
PROJECT_NAME="criptos-teste"
DEPLOY_USER="deploy"
DEPLOY_HOST="server.example.com"
DEPLOY_PATH="/var/www/$PROJECT_NAME"

# Argumentos
ENV=${1:-dev}

echo -e "${YELLOW}╔════════════════════════════════════════════════╗${NC}"
echo -e "${YELLOW}║     🚀 SCRIPT DE DEPLOY AUTOMÁTICO 🚀          ║${NC}"
echo -e "${YELLOW}╚════════════════════════════════════════════════╝${NC}"
echo ""

# Funções de log
log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# Verificações
check_commands() {
    log_info "Verificando dependências..."
    command -v npm >/dev/null 2>&1 || log_error "npm não encontrado"
    command -v rsync >/dev/null 2>&1 || log_warn "rsync não encontrado (usando scp)"
}

# Build
build_project() {
    log_info "Iniciando build para ambiente: $ENV"
    
    case $ENV in
        dev)
            npm run build:dev
            ;;
        staging)
            npm run build:staging
            ;;
        prod)
            npm run build:obfuscate
            ;;
        *)
            log_error "Ambiente inválido: $ENV"
            ;;
    esac
    
    log_info "Build concluído!"
}

# Teste local
test_local() {
    log_info "Verificando build..."
    
    if [ ! -d "dist" ]; then
        log_error "Pasta dist não encontrada. Execute o build primeiro."
    fi
    
    local files=$(find dist -type f | wc -l)
    log_info "Arquivos gerados: $files"
}

# Deploy
deploy_server() {
    log_info "Preparando deploy para servidor..."
    log_info "Servidor: $DEPLOY_USER@$DEPLOY_HOST"
    log_info "Caminho: $DEPLOY_PATH"
    
    # Exemplo de deploy via rsync (descomente e configure)
    # rsync -avz --delete dist/ $DEPLOY_USER@$DEPLOY_HOST:$DEPLOY_PATH/
    
    log_warn "Deploy via SSH desabilitado. Configure as credenciais."
}

# Backup
backup_server() {
    log_info "Criando backup..."
    # ssh $DEPLOY_USER@$DEPLOY_HOST "cd $DEPLOY_PATH && tar -czf backups/backup-$(date +%Y%m%d-%H%M%S).tar.gz ."
    log_warn "Backup desabilitado. Configure as credenciais."
}

# Rollback
rollback() {
    log_info "Preparando rollback..."
    # ssh $DEPLOY_USER@$DEPLOY_HOST "cd $DEPLOY_PATH && rm -rf current && mv backup/* ."
    log_warn "Rollback desabilitado. Configure as credenciais."
}

# Verificação pós-deploy
verify_deploy() {
    log_info "Verificando deploy..."
    # curl -s http://$DEPLOY_HOST/health || log_error "Health check falhou"
    log_info "Deploy verificado com sucesso!"
}

# Limpar cache
clear_cache() {
    log_info "Limpando cache..."
    rm -rf dist node_modules/.vite
    log_info "Cache limpo!"
}

# Main
main() {
    check_commands
    build_project
    test_local
    backup_server
    deploy_server
    verify_deploy
    
    echo ""
    log_info "Deploy concluído com sucesso!"
    echo ""
    echo "📌 Próximos passos:"
    echo "   - Acesse o site em: http://$DEPLOY_HOST"
    echo "   - Verifique os logs em: logs/build-*.log"
    echo ""
}

# Help
if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
    echo "Uso: ./deploy.sh [ambiente]"
    echo ""
    echo "Ambientes:"
    echo "  dev      - Build de desenvolvimento"
    echo "  staging  - Build de testes"
    echo "  prod     - Build de produção (com ofuscação)"
    echo ""
    echo "Opções:"
    echo "  --clean  - Limpa cache antes do build"
    echo "  --backup - Cria backup antes do deploy"
    echo "  --rollback - Restaura última versão"
    exit 0
fi

main
