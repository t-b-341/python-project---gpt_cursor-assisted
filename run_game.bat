@echo off
REM Launch the latest version of the game using Python

cd /d "%~dp0"

REM Optional: activate virtualenv if you use one
REM call venv\Scripts\activate

python game.py

pause
