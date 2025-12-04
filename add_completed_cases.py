#!/usr/bin/env python3
"""
Adicionar 90 casos concluídos distribuídos durante a semana
30 AVLA + 30 ESSOR + 30 DAYCOVAL
SEM apagar os casos existentes
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from pathlib import Path
from dotenv import load_dotenv
import uuid
from datetime import datetime, timedelta, timezone
import random

# Load environment
ROOT_DIR = Path('backend')
load_dotenv(ROOT_DIR / '.env')

RESPONSAVEIS = [
    "Pedro Carvalho",
    "Ana Silva",
    "Carlos Santos",
    "Maria Oliveira",
    "João Souza"
]

CATEGORIAS = [
    "Técnico",
    "Funcional",
    "Performance",
    "Interface",
    "Integração"
]

async def add_completed_cases():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    print("=" * 80)
    print("➕ ADICIONANDO 90 CASOS CONCLUÍDOS (SEM APAGAR EXISTENTES)")
    print("=" * 80)
    
    # Buscar usuário admin para usar como creator
    admin_user = await db.users.find_one({'role': 'administrador'})
    if not admin_user:
        print("❌ Nenhum usuário admin encontrado.")
        return
    
    creator_id = admin_user['id']
    print(f"✅ Usuário admin encontrado: {admin_user['email']}")
    
    # Verificar casos existentes (NÃO vamos apagar)
    existing_count = await db.cases.count_documents({})
    print(f"📊 Casos existentes no banco: {existing_count}")
    
    # Definir período: últimos 7 dias
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=6)  # 7 dias no total
    
    print(f"\n📅 Distribuindo casos de {start_date.strftime('%d/%m')} a {end_date.strftime('%d/%m')}")
    
    # Seguradoras
    seguradoras = ["AVLA", "ESSOR", "DAYCOVAL"]
    
    print("\n📝 ADICIONANDO CASOS CONCLUÍDOS...")
    print("-" * 80)
    
    total_added = 0
    
    for seguradora in seguradoras:
        print(f"\n  📌 {seguradora}:")
        
        # 30 casos concluídos para cada seguradora
        for i in range(30):
            # Distribuir uniformemente durante a semana (7 dias)
            # 30 casos / 7 dias = ~4-5 casos por dia
            day_offset = (i * 7) // 30  # Distribui proporcionalmente
            hours_offset = random.randint(0, 23)
            minutes_offset = random.randint(0, 59)
            
            created_date = start_date + timedelta(
                days=day_offset,
                hours=hours_offset,
                minutes=minutes_offset
            )
            
            # Data de conclusão: entre 1 e 72 horas após criação
            closed_date = created_date + timedelta(hours=random.randint(1, 72))
            
            caso = {
                "id": str(uuid.uuid4()),
                "jira_id": f"SGSS-{seguradora[:3]}-{str(total_added + 1).zfill(3)}",
                "title": f"Chamado {seguradora} #{i+1} - {random.choice(['Integração', 'Performance', 'Bug', 'Melhoria'])}",
                "description": f"Descrição detalhada do chamado concluído para {seguradora}. Categoria: {random.choice(CATEGORIAS)}",
                "status": "Concluído",
                "responsible": random.choice(RESPONSAVEIS),
                "seguradora": seguradora,
                "category": random.choice(CATEGORIAS),
                "priority": random.choice(["Alta", "Média", "Baixa"]),
                "creator_id": creator_id,
                "created_at": created_date.isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "closed_date": closed_date.isoformat()
            }
            
            await db.cases.insert_one(caso)
            total_added += 1
        
        print(f"    ✅ 30 casos concluídos adicionados ({seguradora})")
    
    # Resumo final
    print("\n" + "=" * 80)
    print("📊 RESUMO DA ADIÇÃO")
    print("=" * 80)
    
    # Contar todos os casos agora
    total_now = await db.cases.count_documents({})
    concluidos = await db.cases.count_documents({"status": "Concluído"})
    pendentes = await db.cases.count_documents({"status": "Pendente"})
    aguardando = await db.cases.count_documents({"status": "Aguardando resposta"})
    
    print(f"\n  ➕ Casos adicionados: {total_added}")
    print(f"  📈 Total de casos no banco: {total_now}")
    print(f"     🟢 Concluídos: {concluidos}")
    print(f"     🟡 Pendentes: {pendentes}")
    print(f"     🟠 Aguardando resposta: {aguardando}")
    
    # Distribuição por seguradora
    print(f"\n  📊 Casos por seguradora:")
    for seg in seguradoras:
        count = await db.cases.count_documents({"seguradora": seg})
        print(f"    • {seg}: {count} casos")
    
    # Taxa de conclusão
    completion_rate = round((concluidos / total_now * 100), 1) if total_now > 0 else 0
    print(f"\n  ✅ Taxa de conclusão: {completion_rate}%")
    
    print("\n✅ ADIÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 80)
    
    client.close()

if __name__ == "__main__":
    asyncio.run(add_completed_cases())
