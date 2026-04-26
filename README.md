# ✈️ Monitor de Passagens Aéreas

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-Automation-2ea44f)](https://playwright.dev/python/)
[![Tests](https://img.shields.io/badge/Tests-pytest-yellow)](https://docs.pytest.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

Monitor automatizado de passagens aéreas com foco no mercado brasileiro. Coleta preços em tempo real, registra histórico e envia alertas automáticos via e-mail.

## 📌 Visão Geral

O sistema consulta rotas definidas por você, registra os preços em um banco de dados SQLite e dispara alertas via e-mail quando o valor atingir o alvo configurado. Ideal para viajantes que querem economizar comprando na melhor oportunidade.

**Tecnologias principais:**
- 🎭 **Playwright**: Automação e scraping de websites
- 📊 **SQLite**: Persistência de histórico de preços
- 📧 **SMTP**: Envio de alertas por e-mail
- 🚀 **GitHub Actions**: Execução automatizada e agendada

## ✨ Funcionalidades

- ✅ Coleta automatizada de preços
- ✅ Histórico completo de variação de passagens
- ✅ Alertas por e-mail com preço-alvo atingido
- ✅ Estatísticas e análise de tendências
- ✅ Execução local ou via GitHub Actions
- ✅ CLI para gerenciamento e consulta de dados
- ✅ Retry automático com backoff
- ✅ Logs estruturados e persistentes
- ✅ Validação robusta de configuração
- ✅ Testes abrangentes (unitários + E2E)

## 🏗️ Estrutura do Projeto

```text
flight-watcher-py/
├── .github/
│   └── workflows/
│       └── daily_check.yml     # Execução agendada no GitHub Actions
├── src/
MonitoramentoPassagensAereas/
│   │   └── db_handler.py       # Gerenciamento do SQLite
│   ├── pages/
│       └── daily_check.yml         # Execução diária agendada
│   │   └── flights_page.py     # Page Objects (seletores e interações)
│   ├── __init__.py
│   ├── config.py                   # Gerenciamento de configuração
│   ├── constants.py                # Constantes globais
│   ├── exceptions.py               # Exceções customizadas
│   ├── database/
│   │   ├── __init__.py
│   │   └── db_handler.py           # Operações no SQLite
│   └── utils/
│   │   ├── __init__.py
│   │   ├── base_page.py            # Classe base Playwright
│   │   └── flights_page.py         # Page Object para scraping
│   ├── conftest.py             # Configurações globais do pytest
│   │   ├── __init__.py
│   │   └── email_service.py        # Envio de e-mails SMTP
│   └── test_db.py              # Testes unitários do banco
│       ├── __init__.py
│       ├── logger.py               # Configuração de logs
│       └── helpers.py              # Funções auxiliares
├── .env.example                # Modelo de variáveis
│   ├── conftest.py                 # Fixtures do pytest
│   ├── test_config.py              # Testes de configuração
│   ├── test_db.py                  # Testes do banco de dados
│   ├── test_scraper.py             # Testes de scraping
│   └── test_services.py            # Testes de serviços
├── main.py                         # Ponto de entrada principal
├── cli.py                          # Interface de linha de comando
├── requirements.txt                # Dependências
├── requirements-dev.txt            # Dependências de desenvolvimento
└── README.md
```
├── .gitignore
├── .editorconfig                   # Configuração de editor
├── .pre-commit-config.yaml         # Pre-commit hooks
├── pytest.ini                      # Configuração pytest
├── LICENSE                         # Licença MIT
├── README.md                       # Este arquivo
├── DEVELOPMENT.md                  # Guia de desenvolvimento
├── CHANGELOG.md                    # Histórico de mudanças
└── TROUBLESHOOTING.md              # Solução de problemas

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
EMAIL_USER=gabrielcirinom@gmail.com
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

## 🖥️ Interface de Linha de Comando (CLI)

Gerencie dados e configure o sistema via CLI:

```bash
# Testar conexão com servidor SMTP
python cli.py test-email

# Exibir estatísticas dos últimos 30 dias
python cli.py stats -d 30

# Exibir histórico de preços
python cli.py history -d 7 -l 10

# Limpar registros com mais de 90 dias
python cli.py clear -d 90
```

## 🤝 Contribuição

Contribuições são bem-vindas.

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Abra um pull request com uma descrição clara das mudanças

Para mais detalhes, consulte [DEVELOPMENT.md](DEVELOPMENT.md).

## 📄 Licença

Este projeto está sob a licença MIT.

Para mais detalhes, consulte [LICENSE](LICENSE).

## 📚 Documentação Adicional

- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Guia completo para desenvolvedores
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Solução de problemas e FAQ
- **[CHANGELOG.md](CHANGELOG.md)** - Histórico de mudanças

## 🆘 Suporte

Tem dúvidas ou encontrou um problema?

1. Consulte [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Verifique os logs em `logs/monitor.log`
3. Abra uma [issue no GitHub](https://github.com/seu-usuario/MonitoramentoPassagensAereas/issues)

---

**Made with ❤️ para viajantes que querem economizar** ✈️