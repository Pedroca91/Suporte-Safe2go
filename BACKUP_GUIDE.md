# 📦 Guia de Backup e Restore - Sistema Safe2Go

Este guia explica como fazer backup, restore e exportação dos dados do MongoDB.

---

## 🎯 Scripts Disponíveis

### 1. **backup_mongodb.py** - Backup Completo
Faz backup completo de todas as coleções em formato JSON.

### 2. **restore_mongodb.py** - Restaurar Backup
Restaura dados de um backup anterior.

### 3. **export_csv.py** - Exportar para CSV
Exporta dados para CSV (para análise em Excel/Sheets).

---

## 📖 Como Usar

### 🔹 **Fazer Backup Completo**

```bash
cd /app
python backup_mongodb.py
```

**O que acontece:**
- ✅ Cria pasta `backups/backup_YYYYMMDD_HHMMSS/`
- ✅ Exporta todas as coleções para JSON
- ✅ Cria arquivo `metadata.json` com informações do backup
- ✅ Mostra estatísticas (tamanho, coleções, etc)

**Exemplo de saída:**
```
🔧 Conectando ao MongoDB...
📦 Iniciando backup em: backups/backup_20251127_180530

📋 Coleções encontradas: 5

📥 Fazendo backup: users
  📊 users: 3 documentos
  ✅ Salvo em: backups/backup_20251127_180530/users.json

📥 Fazendo backup: cases
  📊 cases: 15 documentos
  ✅ Salvo em: backups/backup_20251127_180530/cases.json

🎉 Backup concluído com sucesso!
📂 Localização: backups/backup_20251127_180530
💾 Tamanho total: 2.34 MB
📊 Coleções: 5
```

---

### 🔹 **Restaurar Backup**

```bash
cd /app
python restore_mongodb.py backups/backup_20251127_180530
```

**⚠️ ATENÇÃO:** Isso irá **SUBSTITUIR** os dados atuais!

**O que acontece:**
- ⚠️  Pede confirmação
- 🗑️  Remove dados existentes de cada coleção
- 📥 Importa dados do backup
- ✅ Mostra progresso e resultado

**Exemplo:**
```bash
# Listar backups disponíveis
python restore_mongodb.py

# Restaurar backup específico
python restore_mongodb.py backups/backup_20251127_180530
```

---

### 🔹 **Exportar para CSV**

```bash
# Exportar todas as coleções
cd /app
python export_csv.py

# Exportar coleções específicas
python export_csv.py users cases comments
```

**O que acontece:**
- ✅ Cria pasta `exports/export_YYYYMMDD_HHMMSS/`
- ✅ Exporta cada coleção para arquivo CSV separado
- ✅ Arquivos podem ser abertos no Excel, Google Sheets, etc

**Arquivos gerados:**
```
exports/export_20251127_183045/
  ├── users.csv
  ├── cases.csv
  ├── comments.csv
  ├── notifications.csv
  └── activities.csv
```

---

## 📁 Estrutura de Pastas

```
/app/
├── backups/              # Backups em JSON
│   ├── backup_20251127_180530/
│   ├── backup_20251127_190000/
│   └── ...
│
├── exports/              # Exportações CSV
│   ├── export_20251127_183045/
│   └── ...
│
├── backup_mongodb.py     # Script de backup
├── restore_mongodb.py    # Script de restore
└── export_csv.py         # Script de exportação CSV
```

---

## 🔄 Rotina Recomendada

### **Backup Diário:**
```bash
# Executar todo dia às 2h da manhã (exemplo)
python backup_mongodb.py
```

### **Backup Antes de Mudanças:**
```bash
# Antes de fazer qualquer alteração importante
python backup_mongodb.py
```

### **Exportação Mensal:**
```bash
# Todo mês para análise/relatórios
python export_csv.py
```

---

## 💡 Dicas Importantes

### ✅ **Boas Práticas:**

1. **Faça backup ANTES de:**
   - Atualizar o sistema
   - Fazer mudanças no banco
   - Deletar dados
   - Migrar para outro servidor

2. **Mantenha múltiplos backups:**
   - Último backup do dia
   - Backup semanal
   - Backup mensal

3. **Teste o restore periodicamente:**
   - Garante que os backups funcionam
   - Pratique o processo de recuperação

4. **Guarde backups fora do servidor:**
   - Faça download dos backups
   - Guarde em cloud (Google Drive, Dropbox)
   - Mantenha cópias locais

### ⚠️ **Cuidados:**

1. **Restore apaga dados atuais!**
   - Sempre faça backup antes de restore
   - Confirme a pasta correta

2. **Backups ocupam espaço:**
   - Limpe backups antigos periodicamente
   - Comprima backups grandes

3. **Senhas no metadata.json:**
   - Parte da senha é ocultada automaticamente
   - Não compartilhe metadata.json

---

## 🆘 Solução de Problemas

### **Erro: "Nenhuma coleção encontrada"**
**Causa:** Banco vazio ou nome incorreto  
**Solução:** Verifique MONGO_URL e DB_NAME no `.env`

### **Erro: "Permission denied"**
**Causa:** Falta de permissão para criar pastas  
**Solução:** Execute com permissões adequadas

### **Backup muito grande**
**Causa:** Muitos dados acumulados  
**Solução:** 
- Exporte para CSV (menor)
- Comprima a pasta de backup (zip)

---

## 📞 Comandos Rápidos

```bash
# Backup rápido
python backup_mongodb.py

# Ver backups disponíveis
ls -lh backups/

# Restaurar último backup
python restore_mongodb.py backups/$(ls -t backups/ | head -1)

# Exportar apenas usuários e chamados
python export_csv.py users cases

# Comprimir backup
cd backups
tar -czf backup_20251127.tar.gz backup_20251127_180530/
```

---

## 📊 Exemplo Completo

```bash
# 1. Fazer backup
python backup_mongodb.py
# Resultado: backups/backup_20251127_180530/

# 2. Fazer mudanças no sistema...
# (adicionar dados, editar, etc)

# 3. Se algo der errado, restaurar:
python restore_mongodb.py backups/backup_20251127_180530
# Confirma: sim

# 4. Exportar para análise
python export_csv.py
# Resultado: exports/export_20251127_183045/

# 5. Abrir no Excel/Sheets
# Arquivos CSV prontos para uso!
```

---

## 🎯 Resumo

| Script | Função | Quando Usar |
|--------|--------|-------------|
| `backup_mongodb.py` | Backup completo JSON | Antes de mudanças, diariamente |
| `restore_mongodb.py` | Restaurar dados | Quando precisar voltar no tempo |
| `export_csv.py` | Exportar para análise | Relatórios, compartilhar dados |

**💡 Lembre-se:** Backup é como seguro - melhor ter e não precisar!

---

**Última atualização:** 27 de Novembro de 2025
