@echo off
chcp 65001 >nul 2>&1
REM Script para subir el proyecto a GitHub
REM Maquetador de EPUB Accesibles
REM Repositorio: https://github.com/hxebolax/maquetador-epub-accesible

setlocal enabledelayedexpansion

echo ========================================
echo Maquetador de EPUB Accesibles
echo Subir a GitHub
echo ========================================
echo.

REM Cambiar al directorio raiz del proyecto
cd /d "%~dp0.."

REM Verificar que Git esta instalado
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git no esta instalado o no esta en el PATH.
    echo Descargue Git desde: https://git-scm.com/downloads
    pause
    exit /b 1
)

REM Configurar Git para usar UTF-8
git config --global core.quotepath false >nul 2>&1
git config --global i18n.commitencoding utf-8 >nul 2>&1
git config --global i18n.logoutputencoding utf-8 >nul 2>&1

echo Git encontrado.
echo.

REM Verificar si ya existe un repositorio Git
if exist ".git" (
    echo Repositorio Git existente detectado.
    echo.
    goto :actualizar
) else (
    echo No se encontro repositorio Git.
    echo.
    goto :primera_vez
)

:primera_vez
echo ========================================
echo PRIMERA VEZ - Inicializando repositorio
echo ========================================
echo.

REM Inicializar repositorio
echo Inicializando repositorio Git...
git init
if errorlevel 1 (
    echo ERROR: No se pudo inicializar el repositorio.
    pause
    exit /b 1
)

REM Agregar todos los archivos
echo.
echo Agregando archivos...
git add .

REM Hacer commit inicial
echo.
set /p mensaje_commit="Mensaje del commit (Enter para 'Initial commit'): "
if "!mensaje_commit!"=="" set mensaje_commit=Initial commit: Maquetador de EPUB Accesibles v2.0.0

git commit -m "!mensaje_commit!"
if errorlevel 1 (
    echo ERROR: No se pudo hacer el commit.
    pause
    exit /b 1
)

REM Renombrar rama a main
echo.
echo Configurando rama main...
git branch -M main

REM Agregar remote
echo.
echo Agregando repositorio remoto...
git remote add origin https://github.com/hxebolax/maquetador-epub-accesible.git
if errorlevel 1 (
    echo Nota: El remote ya existe o hubo un error.
    git remote set-url origin https://github.com/hxebolax/maquetador-epub-accesible.git
)

REM Push inicial
echo.
echo Subiendo a GitHub...
git push -u origin main
if errorlevel 1 (
    echo.
    echo ERROR: No se pudo subir a GitHub.
    echo Verifique:
    echo   1. Que tiene acceso al repositorio
    echo   2. Que esta autenticado en Git
    echo   3. Que el repositorio existe en GitHub
    echo.
    echo Si el repositorio ya tiene contenido, use:
    echo   git push -u origin main --force
    pause
    exit /b 1
)

echo.
echo ========================================
echo Subida inicial completada!
echo ========================================
goto :fin

:actualizar
echo ========================================
echo ACTUALIZACION - Subiendo cambios
echo ========================================
echo.

REM Mostrar estado
echo Estado actual del repositorio:
echo.
git status --short
echo.

REM Preguntar si continuar
set /p continuar="Desea continuar con la subida? (S/N): "
if /i not "!continuar!"=="S" (
    echo Operacion cancelada.
    pause
    exit /b 0
)

REM Agregar todos los cambios
echo.
echo Agregando cambios...
git add .

REM Verificar si hay cambios para commit
git diff --cached --quiet
if not errorlevel 1 (
    echo No hay cambios nuevos para subir.
    pause
    exit /b 0
)

REM Pedir mensaje de commit
echo.
set /p mensaje_commit="Mensaje del commit: "
if "!mensaje_commit!"=="" (
    echo ERROR: Debe proporcionar un mensaje de commit.
    pause
    exit /b 1
)

REM Hacer commit
git commit -m "!mensaje_commit!"
if errorlevel 1 (
    echo ERROR: No se pudo hacer el commit.
    pause
    exit /b 1
)

REM Push
echo.
echo Subiendo a GitHub...
git push
if errorlevel 1 (
    echo.
    echo ERROR: No se pudo subir a GitHub.
    echo.
    echo Intentando pull primero...
    git pull --rebase
    git push
    if errorlevel 1 (
        echo ERROR: Sigue fallando. Revise los conflictos manualmente.
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo Actualizacion completada!
echo ========================================

:fin
echo.
echo Repositorio: https://github.com/hxebolax/maquetador-epub-accesible
echo.
pause
