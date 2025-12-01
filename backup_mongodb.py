#!/usr/bin/env python3
"""
Script de Backup Completo do MongoDB
Exporta todas as coleções para arquivos JSON
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load environment
ROOT_DIR = Path('backend')
load_dotenv(ROOT_DIR / '.env')

# Diretório de backups
BACKUP_DIR = Path('backups')
BACKUP_DIR.mkdir(exist_ok=True)

async def backup_collection(db, collection_name, backup_path):
    """Faz backup de uma coleção específica"""
    try:
        collection = db[collection_name]
        
        # Contar documentos
        count = await collection.count_documents({})
        print(f"  📊 {collection_name}: {count} documentos")
        
        if count == 0:
            print(f"  ⚠️  Coleção vazia, pulando...")
            return
        
        # Buscar todos os documentos
        cursor = collection.find({})
        documents = await cursor.to_list(length=None)
        
        # Converter ObjectId e datetime para strings
        for doc in documents:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])
            # Converter campos datetime
            for key, value in doc.items():
                if isinstance(value, datetime):
                    doc[key] = value.isoformat()
        
        # Salvar em JSON
        file_path = backup_path / f"{collection_name}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(documents, f, indent=2, ensure_ascii=False)
        
        print(f"  ✅ Salvo em: {file_path}")
        
    except Exception as e:
        print(f"  ❌ Erro ao fazer backup de {collection_name}: {e}")

async def main():
    mongo_url = os.environ['MONGO_URL']
    db_name = os.environ['DB_NAME']
    
    print("🔧 Conectando ao MongoDB...")
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    # Criar pasta com timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = BACKUP_DIR / f"backup_{timestamp}"
    backup_path.mkdir(exist_ok=True)
    
    print(f"📦 Iniciando backup em: {backup_path}\n")
    
    # Listar todas as coleções
    collections = await db.list_collection_names()
    
    if not collections:
        print("⚠️  Nenhuma coleção encontrada no banco!")
        return
    
    print(f"📋 Coleções encontradas: {len(collections)}\n")
    
    # Fazer backup de cada coleção
    for collection_name in collections:
        print(f"📥 Fazendo backup: {collection_name}")
        await backup_collection(db, collection_name, backup_path)
        print()
    
    # Criar arquivo de metadata
    metadata = {
        'backup_date': datetime.now().isoformat(),
        'database_name': db_name,
        'collections': collections,
        'mongo_url': mongo_url.split('@')[0] + '@***'  # Ocultar senha
    }
    
    metadata_path = backup_path / 'metadata.json'
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"📄 Metadata salvo em: {metadata_path}")
    
    # Estatísticas
    total_size = sum(f.stat().st_size for f in backup_path.glob('*.json'))
    size_mb = total_size / (1024 * 1024)
    
    print(f"\n🎉 Backup concluído com sucesso!")
    print(f"📂 Localização: {backup_path}")
    print(f"💾 Tamanho total: {size_mb:.2f} MB")
    print(f"📊 Coleções: {len(collections)}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(main())
