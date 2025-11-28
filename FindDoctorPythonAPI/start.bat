@echo off
echo ===============================================
echo   FindDoctor Python API - Inicializacao
echo ===============================================
echo.

REM Verifica se Python esta instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao encontrado! Instale Python 3.8+ primeiro.
    pause
    exit /b 1
)

echo [1/3] Instalando dependencias...
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao instalar dependencias!
    pause
    exit /b 1
)

echo.
echo [2/3] Verificando banco de dados...
echo Certifique-se que PostgreSQL esta rodando na porta 6025
echo.

echo [3/3] Iniciando API...
echo.
echo API disponivel em: http://localhost:8000
echo Documentacao: http://localhost:8000/docs
echo.
echo Pressione Ctrl+C para parar
echo.

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause
