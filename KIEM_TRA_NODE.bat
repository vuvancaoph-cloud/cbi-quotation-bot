@echo off
chcp 65001 > nul
echo Kiem tra Node.js va npm:
node --version 2>nul && echo [OK] Node.js co san || echo [KHONG CO] Node.js chua duoc cai
npm --version 2>nul && echo [OK] npm co san || echo [KHONG CO] npm chua duoc cai
echo.
pause
