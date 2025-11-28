"""
Script para instalar dependências e iniciar a API
"""
import subprocess
import sys
import os

def main():
    print("=" * 60)
    print("🚀 FindDoctor Python API - Setup e Inicialização")
    print("=" * 60)
    
    # Verifica se está na pasta correta
    if not os.path.exists("requirements.txt"):
        print("❌ Erro: Execute este script na pasta FindDoctorPythonAPI")
        sys.exit(1)
    
    # Instala dependências
    print("\n📦 Instalando dependências...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        sys.exit(1)
    
    # Inicia a API
    print("\n🚀 Iniciando a API FastAPI...")
    print("📍 A API estará disponível em: http://localhost:8000")
    print("📚 Documentação: http://localhost:8000/docs")
    print("🔍 Pressione Ctrl+C para parar\n")
    
    try:
        subprocess.run([sys.executable, "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"])
    except KeyboardInterrupt:
        print("\n\n👋 API encerrada!")
    except Exception as e:
        print(f"\n❌ Erro ao iniciar API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
