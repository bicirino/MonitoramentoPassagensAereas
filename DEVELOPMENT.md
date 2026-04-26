# 🛠️ Guia de Desenvolvimento

Este documento descreve como configurar o ambiente de desenvolvimento e contribuir para o projeto.

## 📋 Pré-requisitos

- Python 3.11+
- Git
- Ambiente virtual (recomendado)

## ⚙️ Setup Inicial

### 1. Clonar o repositório
```bash
git clone <url-do-repositorio>
cd MonitoramentoPassagensAereas
```

### 2. Criar e ativar ambiente virtual
```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows (PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Instalar dependências
```bash
# Dependências base
pip install -r requirements.txt

# Dependências de desenvolvimento
pip install -r requirements-dev.txt

# Instalar navegador do Playwright
playwright install chromium
```

### 4. Configurar arquivo .env
```bash
cp .env.example .env
# Edite .env com suas credenciais
```

## 🧪 Rodando Testes

```bash
# Todos os testes
pytest

# Com cobertura
pytest --cov=src

# Modo verbose
pytest -v

# Testes específicos
pytest tests/test_db.py

# Com visualização do navegador (E2E)
RUN_E2E=1 pytest tests/test_scraper.py --headed
```

## 🎨 Formatação e Qualidade de Código

```bash
# Formatar código com Black
black src/ tests/ main.py

# Verificar estilo com Flake8
flake8 src/ tests/ main.py

# Ordenar imports com isort
isort src/ tests/ main.py

# Verificar tipos com mypy
mypy src/
```

## 📝 Estrutura de Commits

Use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/):

```
feat: Adiciona nova funcionalidade
fix: Corrige um bug
docs: Atualiza documentação
test: Adiciona testes
refactor: Refatora código sem mudar funcionalidade
perf: Melhora performance
chore: Mudanças de build, dependências, etc
```

Exemplos:
```bash
git commit -m "feat: adiciona retry automático no scraping"
git commit -m "fix: corrige parsing de preço em formato brasileiro"
git commit -m "test: adiciona cobertura para db_handler"
```

## 🔄 Fluxo de Contribuição

1. **Crie uma branch** para sua feature/fix:
   ```bash
   git checkout -b feat/sua-feature
   ```

2. **Desenvolva e teste** suas mudanças:
   ```bash
   pytest
   black src/ tests/
   flake8 src/ tests/
   ```

3. **Commit** com mensagem descritiva:
   ```bash
   git commit -m "feat: descrição da feature"
   ```

4. **Push** para sua branch:
   ```bash
   git push origin feat/sua-feature
   ```

5. **Abra um Pull Request** com descrição clara

## 📚 Estrutura do Projeto

```
src/
├── __init__.py
├── config.py              # Gerenciamento de configuração
├── constants.py           # Constantes do projeto
├── exceptions.py          # Exceções customizadas
├── database/
│   ├── __init__.py
│   └── db_handler.py      # Operações no banco de dados
├── pages/
│   ├── __init__.py
│   ├── base_page.py       # Classe base do Playwright
│   └── flights_page.py    # Page Object específico
├── services/
│   ├── __init__.py
│   └── email_service.py   # Envio de e-mails
└── utils/
    ├── __init__.py
    └── logger.py          # Configuração de logs

tests/
├── conftest.py            # Fixtures do pytest
├── test_config.py         # Testes de configuração
├── test_db.py             # Testes do banco de dados
├── test_scraper.py        # Testes de scraping
└── test_services.py       # Testes de serviços
```

## 🐛 Debug

### Ativar logs de debug
```bash
# Edite o logger para incluir DEBUG
# Ou execute com variável de ambiente
DEBUG=1 python main.py
```

### Rodar com browser visível
```bash
# Edite .env: HEADLESS=false
python main.py
```

### Inspecionar banco de dados
```bash
python
>>> from src.database.db_handler import FlightPriceDB
>>> db = FlightPriceDB()
>>> db.get_statistics("GRU", "FLN")
```

## 📖 Documentação do Código

Todas as funções devem ter docstrings no formato Google:

```python
def minha_funcao(param1: str, param2: int) -> bool:
    """Descrição breve da função.
    
    Descrição mais longa se necessário.
    
    Args:
        param1: Descrição do primeiro parâmetro
        param2: Descrição do segundo parâmetro
        
    Returns:
        bool: Descrição do retorno
        
    Raises:
        ValueError: Quando algo inválido ocorre
    """
    pass
```

## 🚀 Publicar uma Release

1. Atualizar versão em `src/__init__.py` (se houver)
2. Atualizar `CHANGELOG.md`
3. Criar tag:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

## ❓ Perguntas ou Problemas?

Abra uma issue no GitHub descrevendo o problema ou dúvida de forma clara.

---

**Obrigado por contribuir!** 🎉
