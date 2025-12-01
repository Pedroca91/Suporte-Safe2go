# 📦 Guia Rápido de Backup - Safe2Go

## 🚀 Comandos Essenciais

### Fazer Backup Completo
```bash
cd /app
python backup_mongodb.py
```

### Restaurar Backup
```bash
cd /app
python restore_mongodb.py backups/backup_YYYYMMDD_HHMMSS
```

### Exportar para CSV
```bash
cd /app
python export_csv.py
```

### Backup Automático (com limpeza)
```bash
cd /app
./auto_backup.sh
```

---

## 📂 Onde Estão os Arquivos?

| Tipo | Localização | Descrição |
|------|-------------|-----------|
| **Backups JSON** | `/app/backups/` | Backup completo de todas as coleções |
| **Exportações CSV** | `/app/exports/` | Arquivos para Excel/Sheets |

---

## 💡 Quando Fazer Backup?

✅ **SEMPRE antes de:**
- Atualizar o sistema
- Deletar dados
- Fazer mudanças importantes
- Migrar servidor

✅ **Regularmente:**
- Diariamente (automático)
- Semanalmente (manual)
- Antes de cada manutenção

---

## 📥 Download de Backup

Para baixar os backups para sua máquina local, você pode:

1. **Via Interface Emergent**: 
   - Ir em "Files" no menu
   - Navegar até `/app/backups/`
   - Download da pasta desejada

2. **Via Script** (se tiver acesso SSH):
   ```bash
   # Comprimir backup
   cd /app/backups
   tar -czf backup_hoje.tar.gz backup_20251201_203211/
   
   # Baixar o .tar.gz
   ```

---

## ⚠️ IMPORTANTE

- **Backups JSON** = Para restaurar no MongoDB
- **Exportações CSV** = Para análise/relatórios no Excel
- **Metadata.json** = Informações sobre o backup

**Guarde seus backups em local seguro!**

---

## 🆘 Ajuda Rápida

**Ver backups disponíveis:**
```bash
ls -lh /app/backups/
```

**Ver última exportação:**
```bash
ls -lh /app/exports/
```

**Espaço ocupado:**
```bash
du -sh /app/backups/
du -sh /app/exports/
```

---

📖 **Guia Completo:** Veja `BACKUP_GUIDE.md` para detalhes
