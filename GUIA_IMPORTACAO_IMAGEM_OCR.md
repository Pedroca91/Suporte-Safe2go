# 🖼️ Guia de Importação via Imagem com OCR

## 📋 Visão Geral

O sistema Safe2Go possui funcionalidade de **OCR (Optical Character Recognition)** que permite importar casos diretamente de screenshots ou imagens de tabelas. O sistema usa **Tesseract.js** configurado para português.

---

## ✅ Melhorias Implementadas

### Versão Anterior (Problemas)
- ❌ Parser muito simplista
- ❌ Não reconhecia variações de IDs (SGSS-N012, SGSS N012)
- ❌ Baixa taxa de extração de casos
- ❌ Poucos logs para debug
- ❌ Não detectava status e responsáveis corretamente

### Versão Nova (Melhorias)
- ✅ **Parser inteligente** com múltiplos padrões de ID
- ✅ **Suporte para variações**: SGSS-N012, SGSS N012, WEB-732303
- ✅ **Detecção automática de**:
  - Status (Aguardando Suporte, Em Atendimento, Concluído)
  - Responsável (nomes de pessoas)
  - Categoria/Organização (DAIG, AIPEAT, AVLA, etc)
- ✅ **Logs detalhados** no console do navegador
- ✅ **Verificação de duplicados** por jira_id
- ✅ **Configuração otimizada** do Tesseract para tabelas
- ✅ **Feedback em tempo real** do processo

---

## 📸 Como Tirar um Screenshot Ideal

Para **melhor resultado** do OCR:

### ✅ BOM
1. **Alta resolução**: Tire screenshot em tela cheia
2. **Contraste**: Fundo claro, texto escuro (ou vice-versa)
3. **Foco**: Apenas a tabela, sem elementos extras
4. **Zoom adequado**: Texto legível mas não pixelado
5. **Sem cortes**: IDs e títulos completos visíveis

### ❌ EVITAR
1. ❌ Imagens desfocadas ou borradas
2. ❌ Texto muito pequeno (< 12px)
3. ❌ Baixo contraste (cinza sobre branco)
4. ❌ Elementos sobrepostos (popups, modals)
5. ❌ Ângulos inclinados

---

## 🚀 Passo a Passo

### 1. Preparar a Imagem
```
✅ Tire um screenshot da tabela de casos
✅ Salve em formato PNG ou JPG
✅ Verifique se está legível
```

### 2. Importar no Sistema
1. Faça login como **administrador**
2. Vá para página **Chamados**
3. Clique em **"Importar"**
4. Selecione sua **imagem** (.png, .jpg, etc)
5. Aguarde o processamento (pode levar 10-30 segundos)

### 3. Acompanhar o Processo
- Abra o **Console do navegador** (F12 → Console)
- Veja os logs em tempo real:
  - `🖼️ Iniciando OCR...`
  - `🔄 Reconhecendo texto...`
  - `✅ OCR Completo! Confiança: XX%`
  - `📊 Total de linhas: XX`
  - `✅ Caso encontrado: SGSS-N012 - Título...`
  - `📊 Total de casos extraídos: XX`

### 4. Resultado
- ✅ **Sucesso**: "X chamado(s) criado(s) da imagem!"
- ⚠️ **Duplicados**: "X já existiam"
- ❌ **Erro**: Verifique os logs

---

## 🎯 Formato Esperado da Imagem

O OCR funciona melhor com tabelas que contêm:

### Colunas Reconhecidas
| Coluna | Exemplo | Obrigatório |
|--------|---------|-------------|
| **ID** | SGSS-N012 | ✅ SIM |
| **Título/Resumo** | "Cartão Protegido e PPC1..." | ✅ SIM |
| **Status** | Aguardando Suporte | ❌ Opcional |
| **Responsável** | Lucas Colete da Silva | ❌ Opcional |
| **Organização** | DAIG, AIPEAT | ❌ Opcional |

### Padrões de ID Reconhecidos
```
✅ SGSS-N012
✅ SGSS N012
✅ SGSS-0012
✅ WEB-732303
✅ PROJ-123
✅ Qualquer formato: LETRAS-NÚMEROS
```

---

## 🔍 Troubleshooting

### "Nenhum chamado identificado na imagem"

**Possíveis causas:**
1. 📸 **Imagem de baixa qualidade**
   - Solução: Tire novo screenshot em resolução maior
   
2. 🔤 **IDs não visíveis ou cortados**
   - Solução: Certifique-se que a coluna de IDs está completa
   
3. 📊 **Formato de tabela não reconhecido**
   - Solução: Use export para JSON ao invés de imagem
   
4. 🌐 **Idioma errado**
   - Sistema configurado para português, mas pode ter dificuldades com outros idiomas

### "Erro ao processar imagem"

**Possíveis causas:**
1. 📦 **Arquivo muito grande** (> 10MB)
   - Solução: Comprima a imagem
   
2. 🖼️ **Formato não suportado**
   - Solução: Use PNG, JPG, JPEG, ou WEBP

### Casos criados com dados incompletos

**Explicação:**
- OCR pode não reconhecer todos os campos perfeitamente
- Casos são criados com dados mínimos: ID + Título
- Outros campos recebem valores padrão

**Solução:**
- Edite os casos após importação
- Ou use JSON para dados completos e precisos

---

## 💡 Dicas Importantes

### Quando usar OCR (Imagem)
✅ Tabelas simples com poucos casos (< 20)
✅ Dados visíveis e legíveis
✅ Quando não tem acesso ao export JSON
✅ Para importações rápidas e informais

### Quando usar JSON
✅ Muitos casos (> 20)
✅ Dados complexos ou com caracteres especiais
✅ Quando precisa de 100% de precisão
✅ Para migrações ou backups

---

## 🧪 Testando o OCR

### Console do Navegador (F12)

Após selecionar uma imagem, você verá:

```javascript
📁 Arquivo selecionado: {
  name: "screenshot.png",
  type: "image/png", 
  size: 2048576,
  isJsonFile: false,
  isImageFile: true
}

🖼️ Processando como imagem com OCR
🖼️ Iniciando OCR para arquivo: screenshot.png Tamanho: 2048576
OCR: {status: 'recognizing text', progress: 0.5}
✅ OCR Completo! Confiança: 87
📝 Texto extraído completo: [texto da imagem]
🔍 Iniciando parse do texto OCR...
📊 Total de linhas: 45
✅ Caso encontrado: SGSS-N012 - Cartão Protegido...
✅ Caso encontrado: SGSS-N020 - DADOS ESSASI...
📊 Total de casos extraídos: 11
✅ Casos válidos finais: 11
```

---

## 📊 Comparação: JSON vs Imagem OCR

| Característica | JSON | Imagem OCR |
|----------------|------|------------|
| **Precisão** | ⭐⭐⭐⭐⭐ 100% | ⭐⭐⭐ 70-90% |
| **Velocidade** | ⚡ Rápido | 🐌 Lento (10-30s) |
| **Capacidade** | ♾️ Ilimitado | 📉 < 50 casos |
| **Facilidade** | 📝 Requer export | 📸 Apenas screenshot |
| **Confiabilidade** | ✅ Alta | ⚠️ Média |
| **Uso ideal** | Produção | Testes/Demo |

---

## 🎓 Recomendações

### Para Produção
1. **Use JSON** sempre que possível
2. Mantenha backups em JSON
3. OCR apenas para casos emergenciais

### Para Desenvolvimento/Testes
1. OCR é perfeito para testes rápidos
2. Útil para demonstrações
3. Bom para POCs

---

## 🐛 Debug Avançado

Se o OCR não funcionar, verifique:

```javascript
// No console do navegador:

// 1. Verificar se Tesseract está carregado
console.log(window.Tesseract)

// 2. Ver texto extraído bruto
// (aparece automaticamente nos logs)

// 3. Testar regex de IDs manualmente
const testText = "SGSS-N012 Título do caso";
const pattern = /\b(SGSS[-\s]?N?\d+)\b/i;
console.log(testText.match(pattern));
```

---

## 📞 Suporte

Se continuar tendo problemas:
1. ✅ Verifique os logs do console (F12)
2. ✅ Tente com imagem de melhor qualidade
3. ✅ Use JSON como alternativa
4. ✅ Teste com arquivo de exemplo fornecido

---

## 🎯 Próximos Passos

Após importar via imagem:
1. ✅ Revise os casos criados
2. ✅ Complete informações faltantes
3. ✅ Ajuste status e responsáveis se necessário
4. ✅ Valide que todos os casos foram importados
