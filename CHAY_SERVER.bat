@echo off
chcp 65001 > nul
echo ============================================
echo   Khoi dong CBI Quotation Bot (Local)
echo ============================================
echo.
echo [INFO] Server chay tai: http://localhost:8000
echo [INFO] Kiem tra health: http://localhost:8000/health
echo [INFO] Nhan Ctrl+C de dung server
echo.

cd /d "%~dp0"
uvicorn main:app --reload --port 8000

pause
