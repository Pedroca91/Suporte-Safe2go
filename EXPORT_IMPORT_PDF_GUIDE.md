# 📋 Guia de Export/Import/PDF - Sistema Safe2Go

## 🎯 Funcionalidades Implementadas

### Para ADMINISTRADORES na tela de Chamados

#### 1. 📄 **Gerar Relatório PDF**
Permite selecionar múltiplos chamados e gerar um relatório em PDF.

**Como usar:**
1. Na página de Chamados (/cases), clique em **"Gerar Relatório PDF"**
2. O modo de seleção é ativado (botão muda para "Cancelar Seleção")
3. Checkboxes aparecem em cada chamado
4. Selecione os chamados desejados:
   - Clique nos checkboxes individuais OU
   - Use "Selecionar Todos" para marcar todos
5. Clique no botão **"Gerar PDF (X)"** (X = número selecionado)
6. O PDF será gerado e baixado automaticamente

**Conteúdo do PDF:**
- ✅ Cabeçalho com título e data de geração
- ✅ Total de chamados no relatório
- ✅ Tabela resumida com:
  - ID/Jira ID
  - Título
  - Status
  - Seguradora
  - Responsável
  - Data de abertura
- ✅ Detalhes completos de cada chamado:
  - Título completo
  - Descrição completa
  - Status, seguradora, responsável
  - Data de abertura

**Nome do arquivo:** `chamados_safe2go_YYYY-MM-DD.pdf`

---

#### 2. 💾 **Exportar Todos os Chamados**
Exporta TODOS os chamados do sistema em formato JSON.

**Como usar:**
1. Na página de Chamados, clique em **"Exportar Todos"**
2. Um arquivo JSON será baixado automaticamente
3. Toast mostra: "X chamados exportados com sucesso!"

**Formato do arquivo JSON:**
```json
{
  "export_date": "2025-12-01T20:30:00.000Z",
  "total_cases": 5,
  "cases": [
    {
      "id": "uuid-aqui",
      "jira_id": "WEB-732393",
      "title": "Título do chamado",
      "description": "Descrição...",
      "status": "Pendente",
      "responsible": "Nome",
      "seguradora": "AVLA",
      "category": "Erro Técnico",
      "opened_date": "2025-11-27T...",
      ...
    },
    ...
  ]
}
```

**Nome do arquivo:** `chamados_backup_YYYY-MM-DD.json`

**Para que serve?**
- ✅ Backup completo de todos os chamados
- ✅ Migração de dados para outro sistema
- ✅ Arquivo histórico para auditoria
- ✅ Restaurar chamados deletados acidentalmente

---

#### 3. 📥 **Importar Chamados**
Importa chamados de um arquivo JSON exportado anteriormente.

**Como usar:**
1. Clique no botão **"Importar"**
2. Selecione um arquivo JSON (formato deve ser igual ao exportado)
3. O sistema processará o arquivo:
   - ✅ Novos chamados são adicionados
   - ⚠️ Chamados duplicados (mesmo jira_id) são ignorados
4. Toast mostra resultado: "Importação concluída! X novos, Y ignorados"

**Validações:**
- ❌ Arquivo deve ser JSON válido
- ❌ Deve conter campo "cases" com array de chamados
- ❌ Duplicatas (mesmo jira_id) são ignoradas automaticamente

**Casos de uso:**
- ✅ Restaurar chamados deletados
- ✅ Migrar chamados de outro ambiente
- ✅ Importar dados históricos
- ✅ Recuperar de backup

---

## 🔐 Segurança

### Permissões:
- ✅ **ADMINISTRADOR**: Vê todos os 4 botões
  - Gerar Relatório PDF
  - Exportar Todos
  - Importar
  - Novo Chamado

- ❌ **CLIENTE**: NÃO vê botões de Export/Import/PDF
  - Vê apenas: banner "Meus Chamados" e seus próprios chamados

---

## 💡 Cenários de Uso

### **Cenário 1: Gerar relatório mensal**
```
1. Filtrar chamados por mês (use filtros de data se disponível)
2. Ativar "Gerar Relatório PDF"
3. Clicar em "Selecionar Todos"
4. Gerar PDF
5. Enviar PDF para gerência
```

### **Cenário 2: Backup antes de manutenção**
```
1. Clicar em "Exportar Todos"
2. Salvar arquivo JSON em local seguro
3. Fazer manutenção/atualizações
4. Se necessário, usar "Importar" para restaurar
```

### **Cenário 3: Migração de dados**
```
Servidor Antigo:
1. Exportar Todos os chamados
2. Baixar JSON

Servidor Novo:
1. Importar o arquivo JSON
2. Verificar que todos os chamados foram importados
```

### **Cenário 4: Relatório personalizado**
```
1. Filtrar por seguradora (ex: AVLA)
2. Ativar "Gerar Relatório PDF"
3. Selecionar apenas chamados específicos
4. Gerar PDF customizado
```

### **Cenário 5: Recuperar chamado deletado**
```
1. Usar backup JSON mais recente (Exportar Todos)
2. Importar o arquivo
3. Sistema ignora duplicatas e adiciona apenas o deletado
```

---

## ⚙️ Detalhes Técnicos

### **Bibliotecas Utilizadas:**
- `jspdf` - Geração de PDF
- `jspdf-autotable` - Tabelas no PDF

### **Formato de Dados:**
- **Export:** JSON com metadata + array de casos
- **Import:** Valida estrutura antes de importar
- **PDF:** Gerado client-side (navegador)

### **Performance:**
- PDF: < 5 segundos para até 100 chamados
- Export: Instantâneo
- Import: ~1 segundo por 10 chamados

---

## 🆘 Solução de Problemas

### **"Selecione pelo menos um chamado"**
**Causa:** Tentou gerar PDF sem selecionar chamados  
**Solução:** Selecione pelo menos 1 chamado antes de clicar em "Gerar PDF"

### **"Arquivo inválido! Formato esperado não encontrado"**
**Causa:** Arquivo JSON não tem estrutura correta  
**Solução:** Use apenas arquivos exportados pelo botão "Exportar Todos"

### **"X novos, Y ignorados"**
**Causa:** Alguns chamados já existem no sistema  
**Solução:** Normal! Sistema ignora duplicatas automaticamente

### **PDF não está baixando**
**Causa:** Bloqueador de pop-ups ou problema no navegador  
**Solução:** 
- Permitir pop-ups para o site
- Tentar em navegador diferente
- Verificar pasta de Downloads

### **Botões não aparecem**
**Causa:** Usuário não é administrador  
**Solução:** Fazer login com conta de administrador

---

## 📊 Exemplos Práticos

### **Exemplo 1: Relatório Semanal**
```bash
# Segunda-feira
1. Filtrar chamados da semana passada
2. Gerar Relatório PDF
3. Selecionar todos
4. Enviar PDF para equipe

Resultado: chamados_safe2go_2025-12-01.pdf
```

### **Exemplo 2: Backup Diário**
```bash
# Todo dia às 18h
1. Exportar Todos
2. Salvar em: /backups/chamados_backup_2025-12-01.json
3. Upload para cloud (Google Drive, Dropbox, etc)

Resultado: Backup seguro de todos os chamados
```

### **Exemplo 3: Auditoria Mensal**
```bash
1. Exportar Todos no último dia do mês
2. Renomear: chamados_novembro_2025.json
3. Gerar PDF de todos os chamados
4. Arquivar ambos os arquivos

Resultado: Registro completo do mês
```

---

## 🎯 Resumo de Comandos

| Ação | Botão | Resultado |
|------|-------|-----------|
| Gerar relatório PDF | "Gerar Relatório PDF" | Ativa modo seleção |
| Selecionar chamado | Checkbox individual | Marca 1 chamado |
| Selecionar todos | "Selecionar Todos" | Marca todos visíveis |
| Criar PDF | "Gerar PDF (X)" | Baixa PDF com X chamados |
| Exportar tudo | "Exportar Todos" | Baixa JSON com todos |
| Importar backup | "Importar" | Abre seletor de arquivo |
| Cancelar seleção | "Cancelar Seleção" | Desativa modo seleção |

---

## ✅ Checklist de Uso

**Antes de fazer backup:**
- [ ] Todos os chamados importantes estão no sistema?
- [ ] Status dos chamados estão atualizados?
- [ ] Comentários importantes foram adicionados?

**Ao exportar:**
- [ ] Clicou em "Exportar Todos"?
- [ ] Arquivo JSON foi baixado?
- [ ] Salvou em local seguro?
- [ ] Testou abrir o arquivo JSON?

**Ao importar:**
- [ ] Arquivo é um JSON válido?
- [ ] Foi exportado do Safe2Go?
- [ ] Fez backup antes de importar?
- [ ] Verificou resultado da importação?

**Ao gerar PDF:**
- [ ] Selecionou os chamados corretos?
- [ ] Conferiu o contador (Gerar PDF (X))?
- [ ] PDF foi baixado?
- [ ] Abriu e verificou o conteúdo?

---

**Última atualização:** 01 de Dezembro de 2025  
**Versão:** 1.0  
**Sistema:** Safe2Go Helpdesk
