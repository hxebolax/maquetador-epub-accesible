@echo off
chcp 65001 >nul 2>&1
REM Script para crear una release en GitHub
REM Maquetador de EPUB Accesibles
REM Repositorio: https://github.com/hxebolax/maquetador-epub-accesible
REM
REM REQUISITO: GitHub CLI (gh) debe estar instalado
REM Descarga: https://cli.github.com/

setlocal enabledelayedexpansion

echo ========================================
echo Maquetador de EPUB Accesibles
echo Crear Release en GitHub
echo ========================================
echo.

REM Cambiar al directorio raiz del proyecto
cd /d "%~dp0.."

REM Verificar que GitHub CLI esta instalado
gh --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: GitHub CLI ^(gh^) no esta instalado.
    echo.
    echo Descargue e instale GitHub CLI desde:
    echo https://cli.github.com/
    echo.
    echo Despues de instalar, ejecute: gh auth login
    echo.
    pause
    exit /b 1
)

echo GitHub CLI encontrado.
echo.

REM Verificar autenticacion
gh auth status >nul 2>&1
if errorlevel 1 (
    echo ERROR: No esta autenticado en GitHub CLI.
    echo.
    echo Ejecute: gh auth login
    echo.
    pause
    exit /b 1
)

echo Autenticacion verificada.
echo.

REM Pedir version
set /p VERSION="Ingrese la version (ej: 2.0.0): "
if "!VERSION!"=="" (
    echo ERROR: Debe proporcionar una version.
    pause
    exit /b 1
)

REM Validar formato de version (simple)
echo !VERSION! | findstr /r "^[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*$" >nul
if errorlevel 1 (
    echo ADVERTENCIA: El formato de version no parece ser X.Y.Z
    set /p continuar="Desea continuar de todos modos? (S/N): "
    if /i not "!continuar!"=="S" (
        echo Operacion cancelada.
        pause
        exit /b 0
    )
)

REM Pedir titulo de la release
set /p TITULO="Titulo de la release (Enter para 'Version !VERSION!'): "
if "!TITULO!"=="" set TITULO=Version !VERSION!

REM Pedir descripcion
echo.
echo Ingrese la descripcion de la release (puede ser varias lineas).
echo Escriba FIN en una linea sola para terminar:
echo.

set "DESCRIPCION="
:leer_descripcion
set /p linea=""
if /i "!linea!"=="FIN" goto :fin_descripcion
set "DESCRIPCION=!DESCRIPCION!!linea!%%0A"
goto :leer_descripcion

:fin_descripcion

REM Si no hay descripcion, usar una por defecto
if "!DESCRIPCION!"=="" (
    set "DESCRIPCION=Release version !VERSION! - Maquetador de EPUB Accesibles."
)

echo.
echo ========================================
echo Resumen de la release:
echo ========================================
echo Version: v!VERSION!
echo Titulo: !TITULO!
echo.

REM Preguntar si compilar
set /p COMPILAR="Desea compilar el ejecutable antes de crear la release? (S/N): "

if /i "!COMPILAR!"=="S" (
    echo.
    echo Compilando aplicacion...
    call scripts\compilar.bat
    if errorlevel 1 (
        echo ERROR: La compilacion fallo.
        pause
        exit /b 1
    )
)

REM Verificar si existe el directorio dist
set "ARCHIVO_ZIP="
if exist "dist\MaquetadorEPUB" (
    echo.
    echo Creando archivo ZIP del ejecutable...
    
    REM Crear ZIP usando PowerShell
    set "ARCHIVO_ZIP=MaquetadorEPUB-v!VERSION!-windows.zip"
    
    if exist "!ARCHIVO_ZIP!" del "!ARCHIVO_ZIP!"
    
    powershell -Command "Compress-Archive -Path 'dist\MaquetadorEPUB\*' -DestinationPath '!ARCHIVO_ZIP!' -Force"
    
    if not exist "!ARCHIVO_ZIP!" (
        echo ADVERTENCIA: No se pudo crear el archivo ZIP.
        set "ARCHIVO_ZIP="
    ) else (
        echo Archivo ZIP creado: !ARCHIVO_ZIP!
    )
)

REM Crear tag si no existe
echo.
echo Verificando tag v!VERSION!...
git tag -l "v!VERSION!" | findstr "v!VERSION!" >nul
if errorlevel 1 (
    echo Creando tag v!VERSION!...
    git tag -a "v!VERSION!" -m "!TITULO!"
    git push origin "v!VERSION!"
) else (
    echo Tag v!VERSION! ya existe.
)

REM Crear la release
echo.
echo Creando release en GitHub...

if "!ARCHIVO_ZIP!"=="" (
    REM Sin archivo adjunto
    gh release create "v!VERSION!" ^
        --title "!TITULO!" ^
        --notes "!DESCRIPCION!" ^
        --repo hxebolax/maquetador-epub-accesible
) else (
    REM Con archivo adjunto
    gh release create "v!VERSION!" ^
        --title "!TITULO!" ^
        --notes "!DESCRIPCION!" ^
        --repo hxebolax/maquetador-epub-accesible ^
        "!ARCHIVO_ZIP!#Ejecutable Windows (ZIP)"
)

if errorlevel 1 (
    echo.
    echo ERROR: No se pudo crear la release.
    echo.
    echo Posibles causas:
    echo   - La release ya existe
    echo   - Problemas de autenticacion
    echo   - El repositorio no existe
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Release creada exitosamente!
echo ========================================
echo.
echo URL: https://github.com/hxebolax/maquetador-epub-accesible/releases/tag/v!VERSION!
echo.

REM Limpiar archivo ZIP temporal
if not "!ARCHIVO_ZIP!"=="" (
    if exist "!ARCHIVO_ZIP!" del "!ARCHIVO_ZIP!"
)

pause
