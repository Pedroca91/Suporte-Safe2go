#!/usr/bin/env python3
"""
Inicializar banco PostgreSQL com schema
"""

import asyncio
import asyncpg
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment
ROOT_DIR = Path('backend')
load_dotenv(ROOT_DIR / '.env')

async def init_database():
    postgres_url = os.environ['POSTGRES_URL']
    
    print("🔧 Conectando ao PostgreSQL...")
    print(f"📡 URL: {postgres_url[:50]}...")
    
    try:
        # Conectar ao banco com SSL
        conn = await asyncpg.connect(
            postgres_url,
            ssl='require'
        )
        
        print("✅ Conectado com sucesso!")
        
        # Ler o arquivo SQL
        print("📄 Lendo schema.sql...")
        with open('backend/schema.sql', 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        # Executar o schema
        print("🚀 Criando tabelas...")
        await conn.execute(schema_sql)
        
        print("✅ Tabelas criadas com sucesso!")
        
        # Verificar tabelas criadas
        tables = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        
        print("\n📋 Tabelas criadas:")
        for table in tables:
            print(f"  ✓ {table['table_name']}")
        
        await conn.close()
        print("\n🎉 Banco de dados inicializado com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(init_database())
