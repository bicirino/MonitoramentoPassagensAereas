# ✈️ Monitor de Passagens Aéreas

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-Automation-2ea44f)](https://playwright.dev/python/)
[![Tests](https://img.shields.io/badge/Tests-pytest-yellow)](https://docs.pytest.org/)

Monitor automatizado de passagens aéreas com foco no mercado brasileiro.

O projeto utiliza:

- Playwright para scraping e automação de navegação
- SQLite para persistência do histórico de preços
- SMTP para envio de alertas por e-mail

## 📌 Visão Geral

O sistema consulta rotas definidas por você, registra os preços no banco de dados e dispara alertas quando o valor atingir o alvo configurado.

## ✨ Funcionalidades

- Coleta automatizada de preços
- Histórico de variação de passagens
- Alertas por e-mail com preço-alvo
- Execução local e via GitHub Actions

## 🏗️ Estrutura do Projeto

```text
flight-watcher-py/
├── .github/
│   └── workflows/
│       └── daily_check.yml     # Execução agendada no GitHub Actions
├── src/
│   ├── database/
│   │   └── db_handler.py       # Gerenciamento do SQLite
│   ├── pages/
│   │   ├── base_page.py        # Métodos genéricos do Playwright
│   │   └── flights_page.py     # Page Objects (seletores e interações)
│   ├── services/
│   │   └── email_service.py    # Envio de e-mails
│   └── utils/
│       └── logger.py           # Logs de execução
├── tests/
│   ├── conftest.py             # Configurações globais do pytest
│   ├── test_scraper.py         # Testes de extração (E2E)
│   └── test_db.py              # Testes unitários do banco
├── .env                        # Variáveis sensíveis (não versionar)
├── .env.example                # Modelo de variáveis
├── .gitignore
├── main.py                     # Ponto de entrada
├── requirements.txt
└── README.md
```

## 🚀 Como Começar

### 1) Pré-requisitos

- Python 3.11+
- Recomendado: ambiente virtual (venv)

### 2) Instalação

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar no Linux/macOS
source venv/bin/activate

# Ativar no Windows (PowerShell)
venv\Scripts\Activate.ps1

# Instalar dependências
pip install -r requirements.txt

# Instalar navegador do Playwright
playwright install chromium
```

### 3) Configuração

Copie o arquivo de exemplo e preencha as variáveis:

```bash
cp .env.example .env
```

Exemplo de configuração:

```dotenv
# Busca
ORIGIN=GRU
DESTINATION=FLN
TARGET_PRICE=650.00

# Notificações
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=seu-email@gmail.com
EMAIL_PASS=sua-senha-de-app-do-google
```

No Windows, se preferir, crie o arquivo `.env` manualmente com base no `.env.example`.

## ▶️ Execução

```bash
python main.py
```

## 🗄️ Persistência de Dados

Na primeira execução, o sistema cria automaticamente o arquivo `flights.db`.

Esse banco armazena o histórico de preços para análise da flutuação ao longo do tempo.

## 🧪 Testes

```bash
# Executar todos os testes
pytest

# Executar testes mostrando o navegador
pytest --headed
```

## 🤝 Contribuição

Contribuições são bem-vindas.

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Abra um pull request com uma descrição clara das mudanças