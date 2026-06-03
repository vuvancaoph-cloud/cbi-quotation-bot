@echo off
chcp 65001 > nul
echo ============================================
echo   Push cap nhat Telegram len GitHub
echo ============================================
cd /d "%~dp0"
git add .
git commit -m "Switch to Telegram Bot - remove Zalo"
git push origin main
echo.
echo Xong! Railway se tu deploy trong ~2 phut.
echo.
pause
