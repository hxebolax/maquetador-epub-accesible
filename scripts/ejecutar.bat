@echo off
chcp 65001 >nul 2>&1
REM Script para ejecutar la aplicacion
REM Maquetador de EPUB Accesibles

REM Cambiar al directorio raiz del proyecto
cd /d "%~dp0.."

REM Verificar que existe el entorno virtual
if not exist ".venv\Scripts\activate.bat" (
    echo ERROR: El entorno virtual no existe.
    echo Ejecute primero: scripts\crear_entorno.bat
    pause
    exit /b 1
)

REM Activar entorno virtual y ejecutar
call .venv\Scripts\activate.bat
python main.py
