@echo off
REM Build a self-contained Windows .exe using PyInstaller.
REM Requires Python and PyInstaller installed on the build machine.

cd /d "%~dp0"

echo Cleaning previous build artifacts...
rmdir /s /q build  2>nul
rmdir /s /q dist   2>nul
del /q MyGame.spec 2>nul

echo Building new executable with PyInstaller...
REM Bundle assets folder into the EXE for use with get_resource_path.
pyinstaller --onefile --name MyGame --noconfirm ^
    --add-data "assets;assets" ^
    --add-data "config;config" ^
    game.py

echo.
echo Build complete. New EXE is in dist\MyGame.exe
echo You can share this EXE with other Windows users who do not have Python installed.
echo.

pause
