#!/bin/bash
# Setup script para Linux/macOS

set -e

echo "🚀 Iniciando setup do Monitor de Passagens Aéreas..."

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.11+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Python $PYTHON_VERSION detectado"

# Criar ambiente virtual
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
else
    echo "✓ Ambiente virtual já existe"
fi

# Ativar ambiente virtual
source venv/bin/activate
echo "✓ Ambiente virtual ativado"

# Instalar dependências
echo "📥 Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

echo "📥 Instalando dependências de desenvolvimento..."
pip install -r requirements-dev.txt

# Instalar Playwright
echo "🌐 Instalando navegador Chromium do Playwright..."
playwright install chromium

# Configurar .env
if [ ! -f ".env" ]; then
    echo "📝 Criando arquivo .env..."
    cp .env.example .env
    echo "⚠️  IMPORTANTE: Edite o arquivo .env com suas credenciais!"
else
    echo "✓ Arquivo .env já existe"
fi

# Setup pre-commit hooks
if command -v pre-commit &> /dev/null; then
    echo "🔧 Configurando pre-commit hooks..."
    pre-commit install
else
    echo "ℹ️  pre-commit não está instalado (opcional)"
fi

echo ""
echo "=========================================="
echo "✓ Setup completo!"
echo "=========================================="
echo ""
echo "Próximos passos:"
echo "1. Edite o arquivo .env com suas credenciais"
echo "2. Execute: source venv/bin/activate"
echo "3. Execute: python main.py"
echo ""
echo "Para mais informações, consulte DEVELOPMENT.md"
echo ""
