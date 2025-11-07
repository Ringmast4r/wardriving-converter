@echo off
REM ======================================================================
REM   UNIVERSAL WARDRIVING CONVERTER - INTERACTIVE MODE
REM ======================================================================

setlocal enabledelayedexpansion

REM Setup conversion vault
set VAULT=%~dp0conversion_vault
if not exist "%VAULT%" mkdir "%VAULT%"

REM Check Python once at startup
python --version >nul 2>&1
if errorlevel 1 (
    cls
    echo.
    echo ======================================================================
    echo   ERROR: Python not found!
    echo ======================================================================
    echo.
    echo Please install Python 3.x from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

:MAIN_LOOP
cls
echo.
echo ======================================================================
echo   UNIVERSAL WARDRIVING CONVERTER
echo ======================================================================
echo.
echo Drag a folder into this window and press Enter...
echo (or type the path manually)
echo.
echo Type 'exit' to quit
echo.
echo ----------------------------------------------------------------------
echo.
set /p INPUT_PATH="Folder path: "

REM Remove quotes and extra spaces
set INPUT_PATH=%INPUT_PATH:"=%
set INPUT_PATH=%INPUT_PATH:  = %

REM Fix missing drive letter (common when dragging into CMD)
REM If path starts with :\ then prepend C
if "%INPUT_PATH:~0,2%"==":\" set INPUT_PATH=C%INPUT_PATH%
REM If path starts with :\Users then prepend C
if "%INPUT_PATH:~0,7%"==":\Users" set INPUT_PATH=C%INPUT_PATH%

REM Check for exit
if /i "%INPUT_PATH%"=="exit" (
    echo.
    echo Goodbye!
    timeout /t 2 >nul
    exit /b 0
)

REM Check if path is empty
if "%INPUT_PATH%"=="" (
    echo.
    echo ERROR: No path provided!
    timeout /t 2 >nul
    goto MAIN_LOOP
)

REM Check if path exists
if not exist "%INPUT_PATH%" (
    echo.
    echo ERROR: Path not found!
    echo.
    echo Tried: %INPUT_PATH%
    echo.
    echo TIP: Right-click the folder and copy path, then paste here
    echo.
    pause
    goto MAIN_LOOP
)

REM Check if it's a folder
if not exist "%INPUT_PATH%\*" (
    echo.
    echo ERROR: This is not a folder. Please drag a FOLDER.
    echo.
    pause
    goto MAIN_LOOP
)

:FOLDER_SCAN
echo.
echo ======================================================================
echo   SCANNING FOLDER...
echo ======================================================================
echo.
echo Folder: %INPUT_PATH%
echo.

REM Count files using dir command (more reliable)
set COUNT=0

REM Scan for each extension type
for %%E in (kml kmz csv xml netxml gpsxml txt ns1 nss) do (
    for /f "delims=" %%F in ('dir /b "%INPUT_PATH%\*.%%E" 2^>nul') do (
        set /a COUNT+=1
        echo [!COUNT!] %%F
    )
)

echo.
echo ----------------------------------------------------------------------

if %COUNT%==0 (
    echo.
    echo No supported files found in this folder!
    echo.
    echo Supported formats: .kml .kmz .csv .xml .netxml .txt
    echo.
    pause
    goto MAIN_LOOP
)

echo.
echo Found %COUNT% file(s) ready to convert
echo.
echo What do you want to do?
echo.
echo   1. Convert each file separately (%COUNT% CSVs)
echo   2. MERGE all into ONE master CSV [RECOMMENDED]
echo   3. Cancel and go back
echo.
set /p CHOICE="Enter choice (1-3): "

if "%CHOICE%"=="3" goto MAIN_LOOP

if "%CHOICE%"=="" (
    echo.
    echo ERROR: No choice entered!
    timeout /t 2 >nul
    goto MAIN_LOOP
)

if not "%CHOICE%"=="1" if not "%CHOICE%"=="2" (
    echo.
    echo ERROR: Invalid choice!
    timeout /t 2 >nul
    goto MAIN_LOOP
)

echo.
echo ======================================================================
echo   STARTING CONVERSION...
echo ======================================================================
echo.

REM Create timestamped output folder
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c%%a%%b)
for /f "tokens=1-2 delims=/: " %%a in ('time /t') do (set mytime=%%a%%b)
set mytime=%mytime: =0%
set OUTPUT_FOLDER=%VAULT%\%mydate%_%mytime%
mkdir "%OUTPUT_FOLDER%" 2>nul

if "%CHOICE%"=="1" (
    REM Convert separately
    python "%~dp0universal_wardrive_converter.py" --folder "%INPUT_PATH%"
    if errorlevel 1 (
        echo.
        echo ERROR: Conversion failed!
        pause
        goto MAIN_LOOP
    )
    xcopy /E /I /Y "%INPUT_PATH%\converted\*" "%OUTPUT_FOLDER%\" >nul 2>&1
    rmdir /S /Q "%INPUT_PATH%\converted" 2>nul
) else (
    REM Merge all
    python "%~dp0universal_wardrive_converter.py" --folder "%INPUT_PATH%" --merge
    if errorlevel 1 (
        echo.
        echo ERROR: Conversion failed!
        pause
        goto MAIN_LOOP
    )
    move "%INPUT_PATH%\converted\merged_all.csv" "%OUTPUT_FOLDER%\MERGED_ALL.csv" >nul 2>&1
    rmdir /S /Q "%INPUT_PATH%\converted" 2>nul
)

echo.
echo ======================================================================
echo   *** CONVERSION COMPLETE! ***
echo ======================================================================
echo.
echo   ^>^>^>  ALL FILES CONVERTED SUCCESSFULLY!  ^<^<^<
echo.
echo   Output: conversion_vault\%mydate%_%mytime%\
echo   Files: %COUNT%
echo.
echo   Made with love by ringmast4r ^<3
echo.
echo ======================================================================
echo.
start "" "%OUTPUT_FOLDER%"
echo ----------------------------------------------------------------------
echo What next?
echo.
echo   1. Convert SAME folder again (different option)
echo   2. Choose a DIFFERENT folder
echo   3. Exit
echo.
set /p NEXT="Enter choice (1-3): "

if "%NEXT%"=="1" goto FOLDER_SCAN
if "%NEXT%"=="3" (
    echo.
    echo Goodbye!
    timeout /t 2 >nul
    exit /b 0
)

goto MAIN_LOOP
