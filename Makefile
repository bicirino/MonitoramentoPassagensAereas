.PHONY: help install test lint format clean run cli dev-setup

help:
	@echo "📖 Monitor de Passagens Aéreas - Comandos disponíveis:"
	@echo ""
	@echo "  make install        Instalar dependências"
	@echo "  make dev-setup      Setup completo de desenvolvimento"
	@echo "  make run            Executar o monitor"
	@echo "  make cli            Acessar CLI de gerenciamento"
	@echo "  make test           Rodar testes"
	@echo "  make test-cov       Rodar testes com cobertura"
	@echo "  make test-e2e       Rodar testes E2E"
	@echo "  make lint           Verificar código (flake8)"
	@echo "  make format         Formatar código (black + isort)"
	@echo "  make clean          Limpar arquivos temporários"
	@echo "  make logs           Exibir últimos logs"
	@echo "  make db-stats       Exibir estatísticas do banco"
	@echo "  make db-history     Exibir histórico de preços"
	@echo "  make db-clear       Limpar dados antigos"
	@echo ""

install:
	pip install -r requirements.txt
	playwright install chromium

dev-setup: install
	pip install -r requirements-dev.txt
	@if [ ! -f ".env" ]; then cp .env.example .env; echo "✓ Arquivo .env criado"; fi
	pre-commit install
	@echo "✓ Setup de desenvolvimento completo"

run:
	python main.py

cli:
	python cli.py --help

test:
	pytest -v

test-cov:
	pytest --cov=src --cov-report=html
	@echo "✓ Relatório de cobertura em htmlcov/index.html"

test-e2e:
	RUN_E2E=1 pytest -v tests/test_scraper.py

lint:
	flake8 src/ tests/ main.py cli.py --max-line-length=100

format:
	black src/ tests/ main.py cli.py
	isort src/ tests/ main.py cli.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	@echo "✓ Arquivos temporários removidos"

logs:
	@if [ -f "logs/monitor.log" ]; then tail -20 logs/monitor.log; else echo "Nenhum log encontrado"; fi

db-stats:
	python cli.py stats -d 30

db-history:
	python cli.py history -d 7

db-clear:
	python cli.py clear -d 90

.DEFAULT_GOAL := help
