@echo off
chcp 65001 > nul
echo ============================================
echo   Deploy len Railway bang CLI
echo ============================================
echo.

cd /d "%~dp0"

REM Buoc 1: Cai Railway CLI
echo [1] Dang cai Railway CLI...
npm install -g @railway/cli 2>nul
if errorlevel 1 (
    echo     npm chua co, thu cach khac...
    powershell -Command "iwr https://railway.app/install.sh | iex" 2>nul
)

REM Kiem tra railway da cai chua
railway --version 2>nul
if errorlevel 1 (
    echo [LOI] Chua cai duoc Railway CLI.
    echo Hay thu cai thu cong tai: https://railway.app/cli
    pause
    exit /b 1
)

echo [OK] Railway CLI da san sang.
echo.

REM Buoc 2: Dang nhap Railway
echo [2] Dang mo trinh duyet de dang nhap Railway...
echo     Hay dang nhap bang tai khoan GitHub: vuvancaoph-cloud
echo.
railway login

REM Buoc 3: Ket noi voi project hien tai
echo.
echo [3] Ket noi voi project Railway...
railway link

REM Buoc 4: Deploy
echo.
echo [4] Dang deploy len Railway...
railway up

echo.
echo [5] Lay URL cua service...
railway domain

echo.
echo ============================================
echo   Xong! Copy URL o tren va gui cho tro ly.
echo ============================================
pause
