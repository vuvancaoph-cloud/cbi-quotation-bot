@echo off
chcp 65001 > nul
echo ============================================
echo   Push code len GitHub
echo ============================================
echo.

cd /d "%~dp0"

REM Kiem tra git da init chua
if not exist ".git" (
    echo [INFO] Chua co .git, dang khoi tao...
    git init
    git branch -m main
    git config user.name "Vu Van"
    git config user.email "vuvancaoph@gmail.com"
)

REM Them remote origin
git remote remove origin 2>nul
git remote add origin https://github.com/vuvancaoph-cloud/cbi-quotation-bot.git

REM Add tat ca file (tru nhung gi trong .gitignore)
git add .

REM Commit
git commit -m "Initial commit: CBI Quotation Bot v1.0" 2>nul || (
    echo [INFO] Khong co gi moi de commit.
)

REM Push len GitHub
echo.
echo Dang push len GitHub...
echo [QUAN TRONG] Trinh duyet se mo ra de dang nhap GitHub.
echo Hay dang nhap bang tai khoan: vuvancaoph-cloud
echo.
git push -u origin main

if errorlevel 1 (
    echo.
    echo [LOI] Push that bai. Thu cac buoc sau:
    echo   1. Kiem tra ket noi internet
    echo   2. Dang nhap dung tai khoan GitHub
    echo   3. Chay lai file nay
) else (
    echo.
    echo ============================================
    echo   THANH CONG! Code da len GitHub.
    echo   Kiem tra tai:
    echo   https://github.com/vuvancaoph-cloud/cbi-quotation-bot
    echo ============================================
)

echo.
pause
