@echo off
chcp 65001 > nul
echo ============================================
echo   Cai dat thu vien Python - CBI Bot
echo ============================================
echo.

cd /d "%~dp0"

REM Kiem tra Python
python --version 2>nul
if errorlevel 1 (
    echo [LOI] Chua co Python! Tai ve tai:
    echo   https://www.python.org/downloads/
    echo Chon phien ban 3.11 hoac moi hon.
    pause
    exit /b 1
)

echo [OK] Da tim thay Python.
echo.
echo Dang cai dat thu vien...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [LOI] Cai dat that bai. Thu chay lai voi quyen Admin.
) else (
    echo.
    echo ============================================
    echo   HOAN THANH! Thu vien da duoc cai xong.
    echo   Chay file CHAY_SERVER.bat de khoi dong bot.
    echo ============================================
)

echo.
pause
