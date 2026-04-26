# 🆘 Troubleshooting & FAQ

Soluções para problemas comuns no Monitor de Passagens Aéreas.

## ❌ Erros de Configuração

### "ConfigurationError: EMAIL_USER e EMAIL_PASS não podem estar vazios"

**Solução**: 
1. Verifique se `.env` existe (copie de `.env.example` se necessário)
2. Adicione `EMAIL_USER` e `EMAIL_PASS` com valores válidos
3. Para Gmail, use [senha de app](https://support.google.com/accounts/answer/185833) (requer 2FA)

```env
EMAIL_USER=seu-email@gmail.com
EMAIL_PASS=sua-senha-de-app
```

### "ConfigurationError: FLIGHTS_URL é obrigatório"

**Solução**: Adicione a URL no arquivo `.env`:
```env
FLIGHTS_URL=https://www.google.com/travel/flights
```

### "ConfigurationError: ORIGIN deve ser um código de aeroporto válido"

**Solução**: Códigos devem ter exatamente 3 letras maiúsculas:
```env
ORIGIN=GRU      # ✓ Correto
ORIGIN=gru      # ✗ Será convertido para maiúscula
ORIGIN=GUARULHOS # ✗ Inválido (mais de 3 caracteres)
```

**Códigos comuns de aeroportos brasileiros:**
- GRU: Guarulhos (São Paulo)
- FLN: Florianópolis
- SSA: Salvador
- GIG: Galeão (Rio de Janeiro)
- CNF: Confins (Belo Horizonte)

---

## ❌ Erros de Scraping

### "ScraperError: Falha ao carregar página após 3 tentativas"

**Causas**:
- Sem conexão de internet
- URL inválida ou site fora do ar
- Site bloqueou requisições automatizadas

**Soluções**:
1. Verifique conexão: `ping google.com`
2. Teste URL em um navegador
3. Aguarde um tempo e tente novamente
4. Implemente um proxy se necessário

### "Nenhum preço detectado na página"

**Causas**:
- O site mudou a estrutura HTML
- Conteúdo carregado via JavaScript não foi esperado
- Filtros de busca precisam ser preenchidos

**Soluções**:
1. Rode com `HEADLESS=false` para visualizar:
   ```bash
   HEADLESS=false python main.py
   ```
2. Inspecione o HTML: `page.content()` nos logs
3. Atualize o regex em `src/constants.py`
4. Implemente preenchimento de filtros em `src/pages/flights_page.py`

---

## ❌ Erros de E-mail

### "SMTPAuthenticationError: 535 Authentication failed"

**Solução**:
1. Confirme email e senha corretos
2. Para Gmail: [gere senha de app](https://support.google.com/accounts/answer/185833)
3. Verifique se 2FA está ativado
4. Teste com: `python -m smtplib`

### "Timeout ao conectar ao servidor SMTP"

**Causas**:
- Servidor SMTP inativo
- Porta incorreta
- Firewall bloqueando conexão

**Soluções**:
1. Verifique porta:
   ```env
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587    # TLS
   # ou
   EMAIL_PORT=465    # SSL
   ```
2. Teste manualmente:
   ```bash
   telnet smtp.gmail.com 587
   ```

### "O e-mail foi enviado mas não chegou"

**Verificações**:
1. Procure em spam/lixo eletrônico
2. Verifique se `EMAIL_TO` está correto
3. Teste enviando para o mesmo email que envia

---

## ❌ Erros de Banco de Dados

### "DatabaseError: Erro ao conectar ao banco de dados"

**Possível causa**: Arquivo `flights.db` corrompido

**Solução**:
```bash
# Remova o banco e deixe ser recriado
rm flights.db
python main.py
```

### "database is locked"

**Causa**: Outro processo está usando o banco

**Soluções**:
1. Aguarde alguns segundos
2. Verifique se não há outra instância rodando:
   ```bash
   ps aux | grep main.py
   ```
3. Mate o processo:
   ```bash
   pkill -f "python main.py"
   ```

---

## ❌ Erros no Playwright

### "Error: Chromium not found"

**Solução**: Instale os navegadores do Playwright:
```bash
playwright install chromium
```

### "Timeout: Timeout 60000ms exceeded"

**Solução**: Aumentar timeout em `.env`:
```python
# Em src/constants.py
DEFAULT_TIMEOUT = 120000  # Aumentar para 2 minutos
```

---

## ❓ FAQ - Perguntas Frequentes

### P: O projeto pode monitorar múltiplas rotas simultaneamente?

**R**: Atualmente, a estrutura monitora uma rota por execução. Para múltiplas rotas:
- Crie múltiplas configurações .env
- Execute em paralelo com scripts diferentes
- Ou implemente um loop no `main.py`

### P: Como agendar execução automática?

**R**: 
- **Linux/macOS**: Use `cron`:
  ```bash
  0 10 * * * cd /caminho && python main.py
  ```
- **Windows**: Use Task Scheduler
- **Qualquer plataforma**: Use GitHub Actions (já configurado)

### P: Posso monitorar outros sites de passagens?

**R**: Sim! Estenda `FlightsPage`:
```python
class SkyscannerPage(BasePage):
    def extract_lowest_price(self):
        # Implemente para Skyscanner
        pass
```

### P: Como debugar se algo não está funcionando?

**R**: Ative modo debug:
```bash
# Edite src/utils/logger.py para DEBUG
# ou
HEADLESS=false python main.py
```

### P: É seguro usar minhas credenciais do Gmail?

**R**: 
- **Não** use sua senha principal
- **Use** [senha de app](https://support.google.com/accounts/answer/185833) (mais segura)
- **Não** commite `.env` com credenciais (já está no `.gitignore`)

### P: Qual a melhor hora para agendar?

**R**: Considere:
- Fora de horários de pico dos sites
- Múltiplas vezes ao dia para máxima cobertura
- GitHub Actions padrão: 10:00 UTC (7:00 Brasília no horário padrão)

### P: Como obter suporte?

**R**: 
1. Leia este documento
2. Verifique logs em `logs/monitor.log`
3. Abra uma issue no GitHub com:
   - Erro completo
   - Arquivo `.env` (sem credenciais)
   - Versão do Python
   - Sistema operacional

---

## 📋 Checklist de Debug

Use este checklist quando algo não funcionar:

- [ ] Verificar variáveis de ambiente `.env`
- [ ] Confirmar versão Python (`python --version`)
- [ ] Testar conexão de internet
- [ ] Rodar testes (`pytest`)
- [ ] Verificar logs em `logs/monitor.log`
- [ ] Rodar com `HEADLESS=false` para visualizar
- [ ] Testar credenciais SMTP manualmente
- [ ] Verificar se Playwright está instalado
- [ ] Limpar banco de dados se necessário

---

**Não encontrou sua solução?** Abra uma issue no GitHub! 🎯
