# Monitoramento de Passagens Aéreas

# ✈️ Flight Watcher Py: Monitor de Passagens com Playwright

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/framework-Playwright-green.svg)](https://playwright.dev/python/)
[![pytest](https://img.shields.io/badge/test-pytest-yellow.svg)](https://docs.pytest.org/)

## 📖 Sobre o Projeto
O **Flight Watcher Py** é uma aplicação de automação e monitoramento de preços de passagens aéreas focado no mercado brasileiro (Latam, Gol, Azul). O projeto foi concebido para aplicar conceitos avançados de **Engenharia de Qualidade (QA)**, utilizando **Playwright** para extração de dados e **Pytest** para validação da integridade do sistema.

## 🛠️ Tecnologias
- **Linguagem:** Python 3.11
- **Automação Web:** Playwright
- **Orquestração de Testes:** Pytest
- **Banco de Dados:** SQLite (Armazenamento de histórico de preços)
- **Configuração:** Portabilidade via `.env` (python-dotenv)
- **Notificação:** Protocolo SMTP (Envio de Alertas por E-mail)
- **CI/CD:** GitHub Actions (Execução agendada via Cron Job)

## 📋 Requisitos do Sistema
- [x] **Web Scraping:** Navegação automatizada nos principais portais aéreos.
- [x] **Persistência:** Registro de data, rota e preço no banco `flights.db`.
- [x] **Lógica de Alerta:** Disparo de e-mail caso o preço atual seja inferior ao limite definido pelo usuário.
- [x] **Configuração Segura:** Credenciais de e-mail e rotas armazenadas em variáveis de ambiente.

## 🗄️ Estrutura do Banco de Dados (SQLite)
O sistema utiliza uma tabela `price_history` para permitir análises futuras:
| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| `id` | INTEGER | Chave primária |
| `origin` | TEXT | IATA da cidade de origem |
| `destination` | TEXT | IATA da cidade de destino |
| `price` | REAL | Valor da passagem |
| `date_check` | DATETIME | Data e hora da verificação |

## 🚀 Instalação e Configuração

1. **Clone o repositório:**
   ```bash
   git clone [[[https://github.com/seu-usuario/flight-watcher-py.git](https://github.com/seu-usuario/flight-watcher-py.git)](https://github.com/bicirino/MonitoramentoPassagensAereas.git)](https://github.com/bicirino/MonitoramentoPassagensAereas.git)

Configure o ambiente:
Crie um arquivo .env na raiz do projeto seguindo o modelo:

Snippet de código
# Configurações de Busca
ORIGIN=GRU
DESTINATION=FLN
TARGET_PRICE=800.00

# Configurações de E-mail (SMTP)
EMAIL_HOST=smtp.gmail.com
EMAIL_USER=seu-email@gmail.com
EMAIL_PASS=sua-senha-de-app
Instale as dependências:

Bash
pip install -r requirements.txt
playwright install chromium

🧪 Estratégia de Testes
Para garantir que o scraper não quebre com mudanças nos sites, execute:

Rodar testes de sanidade (Check de seletores):

Bash
pytest tests/test_selectors.py
Rodar testes de integração (Database & Email):

Bash
pytest tests/test_integration.py
⏰ Agendamento
O projeto conta com um workflow do GitHub Actions (.github/workflows/daily_check.yml) que executa o monitoramento automaticamente todos os dias às 08:00 AM (BRT).

Este projeto é parte do meu portfólio de estudos em Testes e Automação.

