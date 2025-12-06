@echo off
chcp 65001 >nul 2>&1
REM Script para crear y configurar el entorno virtual
REM Maquetador de EPUB Accesibles

echo ========================================
echo Maquetador de EPUB Accesibles
echo Configuracion del entorno virtual
echo ========================================
echo.

REM Cambiar al directorio raiz del proyecto
cd /d "%~dp0.."

REM Verificar que Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH.
    echo Por favor, instale Python 3.8 o superior desde https://python.org
    pause
    exit /b 1
)

echo Python encontrado.
echo.

REM Crear entorno virtual si no existe
if not exist ".venv" (
    echo Creando entorno virtual...
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: No se pudo crear el entorno virtual.
        pause
        exit /b 1
    )
    echo Entorno virtual creado.
) else (
    echo Entorno virtual ya existe.
)
echo.

REM Activar entorno virtual
echo Activando entorno virtual...
call .venv\Scripts\activate.bat

REM Actualizar pip
echo Actualizando pip...
python -m pip install --upgrade pip

REM Instalar dependencias
echo.
echo Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Configuracion completada exitosamente!
echo ========================================
echo.
echo Para ejecutar la aplicacion:
echo   1. Abra una terminal en esta carpeta
echo   2. Ejecute: .venv\Scripts\activate
echo   3. Ejecute: python main.py
echo.
echo O simplemente ejecute: scripts\ejecutar.bat
echo.
pause
