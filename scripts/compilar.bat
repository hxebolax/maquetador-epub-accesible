@echo off
REM Script para compilar la aplicacion con PyInstaller
REM Maquetador de EPUB Accesibles

echo ========================================
echo Maquetador de EPUB Accesibles
echo Compilacion con PyInstaller
echo ========================================
echo.

REM Cambiar al directorio raiz del proyecto
cd /d "%~dp0.."

REM Verificar que existe el entorno virtual
if not exist ".venv\Scripts\activate.bat" (
    echo ERROR: El entorno virtual no existe.
    echo Ejecute primero: scripts\crear_entorno.bat
    pause
    exit /b 1
)

REM Activar entorno virtual
call .venv\Scripts\activate.bat

REM Verificar que PyInstaller esta instalado
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Instalando PyInstaller...
    pip install pyinstaller
)

REM Limpiar compilaciones anteriores
echo Limpiando compilaciones anteriores...
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build

REM Compilar
echo.
echo Compilando aplicacion...
pyinstaller --name="MaquetadorEPUB" ^
    --windowed ^
    --onedir ^
    --add-data="src/recursos;src/recursos" ^
    --hidden-import=wx ^
    --hidden-import=ebooklib ^
    --hidden-import=markdown ^
    --hidden-import=bs4 ^
    --hidden-import=lxml ^
    main.py

if errorlevel 1 (
    echo.
    echo ERROR: La compilacion fallo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Compilacion completada!
echo ========================================
echo.
echo El ejecutable se encuentra en: dist\MaquetadorEPUB\
echo.
pause
