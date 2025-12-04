#!/usr/bin/env python3
"""
Restaurar dados do usuário: 15 Pendentes + 5 Aguardando cliente
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from pathlib import Path
from dotenv import load_dotenv
import uuid
from datetime import datetime, timezone

# Load environment
ROOT_DIR = Path('backend')
load_dotenv(ROOT_DIR / '.env')

async def restore_user_data():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    print("=" * 80)
    print("🔄 RESTAURANDO DADOS DO USUÁRIO")
    print("=" * 80)
    
    # Buscar usuário admin para usar como creator
    admin_user = await db.users.find_one({'role': 'administrador'})
    if not admin_user:
        print("❌ Nenhum usuário admin encontrado.")
        return
    
    creator_id = admin_user['id']
    print(f"✅ Usuário admin encontrado: {admin_user['email']}")
    
    # Limpar casos existentes
    await db.cases.delete_many({})
    print(f"✅ Banco limpo.")
    
    # Criar 15 casos PENDENTES
    print(f"\n📝 Criando 15 casos PENDENTES...")
    for i in range(15):
        caso = {
            "id": str(uuid.uuid4()),
            "jira_id": f"PEND-{str(i + 1).zfill(3)}",
            "title": f"Caso Pendente #{i+1}",
            "description": f"Descrição do caso pendente {i+1}",
            "status": "Pendente",
            "responsible": "Equipe Suporte",
            "seguradora": ["AVLA", "ESSOR", "DAYCOVAL"][i % 3],
            "category": "Técnico",
            "priority": "Média",
            "creator_id": creator_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        await db.cases.insert_one(caso)
    
    print(f"   ✅ 15 casos PENDENTES criados")
    
    # Criar 5 casos AGUARDANDO RESPOSTA
    print(f"\n📝 Criando 5 casos AGUARDANDO RESPOSTA...")
    for i in range(5):
        caso = {
            "id": str(uuid.uuid4()),
            "jira_id": f"AGRD-{str(i + 1).zfill(3)}",
            "title": f"Caso Aguardando Cliente #{i+1}",
            "description": f"Descrição do caso aguardando resposta do cliente {i+1}",
            "status": "Aguardando resposta",
            "responsible": "Equipe Suporte",
            "seguradora": ["AVLA", "ESSOR", "DAYCOVAL"][i % 3],
            "category": "Funcional",
            "priority": "Alta",
            "creator_id": creator_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        await db.cases.insert_one(caso)
    
    print(f"   ✅ 5 casos AGUARDANDO RESPOSTA criados")
    
    # Resumo final
    print("\n" + "=" * 80)
    print("📊 RESUMO DA RESTAURAÇÃO")
    print("=" * 80)
    
    total = await db.cases.count_documents({})
    pendentes = await db.cases.count_documents({"status": "Pendente"})
    aguardando = await db.cases.count_documents({"status": "Aguardando resposta"})
    
    print(f"\n  📈 Total de casos no banco: {total}")
    print(f"  🟡 Pendentes: {pendentes}")
    print(f"  🟠 Aguardando resposta: {aguardando}")
    
    print("\n✅ RESTAURAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 80)
    
    client.close()

if __name__ == "__main__":
    asyncio.run(restore_user_data())
