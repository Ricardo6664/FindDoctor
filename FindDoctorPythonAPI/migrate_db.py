"""
Script para adicionar colunas faltantes nas tabelas existentes
Execute uma vez para atualizar o schema do banco
"""
from sqlalchemy import create_engine, text
from config import settings

engine = create_engine(settings.DATABASE_URL)

migrations = [
    # Adicionar coluna is_active na tabela doctors (se não existir)
    """
    DO $$ 
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM information_schema.columns 
            WHERE table_name='doctors' AND column_name='is_active'
        ) THEN
            ALTER TABLE doctors ADD COLUMN is_active BOOLEAN DEFAULT true;
        END IF;
    END $$;
    """,
    # Adicionar coluna crm na tabela doctors (se não existir)
    """
    DO $$ 
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM information_schema.columns 
            WHERE table_name='doctors' AND column_name='crm'
        ) THEN
            ALTER TABLE doctors ADD COLUMN crm VARCHAR(50);
        END IF;
    END $$;
    """,
]

print("🔧 Aplicando migrações no banco de dados...")

with engine.connect() as conn:
    for i, migration in enumerate(migrations, 1):
        try:
            conn.execute(text(migration))
            conn.commit()
            print(f"✅ Migração {i} aplicada com sucesso")
        except Exception as e:
            print(f"❌ Erro na migração {i}: {e}")
            conn.rollback()

print("✅ Migrações concluídas!")
