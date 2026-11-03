@echo off
chcp 65001 >nul
rem Запуск приложения на компьютере (Windows) для проверки внешнего вида до сборки APK.
rem Нужен установленный Python 3.11 или 3.12 (python.org, отметьте "Add Python to PATH").
cd /d "%~dp0"
if not exist .venv (
    py -3.12 -m venv .venv 2>nul || py -3.11 -m venv .venv 2>nul || py -3 -m venv .venv
)
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install kivy==2.3.1 kivymd==1.2.0 plyer==2.1.0 pillow certifi
python main.py
pause
