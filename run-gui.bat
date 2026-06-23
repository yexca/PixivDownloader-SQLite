@echo off

if /i "%cd%"=="C:\Windows\System32" (
    color 0C
    echo PixivDownloader does not require administrator permissions.
    echo Please run this script as a regular user from the project folder.
    echo.
    pause
    exit /b 1
)

setlocal
set "INSTALL_DIR=%~dp0"
set "INSTALL_DIR=%INSTALL_DIR:~0,-1%"
title PixivDownloader GUI

if not exist "%INSTALL_DIR%\env\python.exe" (
    echo Local environment not found.
    echo Please run 'run-install.bat' first to set up the environment.
    echo.
    pause
    exit /b 1
)

cd /d "%INSTALL_DIR%"
"%INSTALL_DIR%\env\python.exe" "%INSTALL_DIR%\main.py"
echo.
pause
