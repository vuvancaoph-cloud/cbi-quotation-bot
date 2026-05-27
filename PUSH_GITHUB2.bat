@echo off
chcp 65001 > nul
echo ============================================
echo   Push code len GitHub (lan 2)
echo ============================================
echo.

cd /d "%~dp0"

REM Xoa .git cu hoan toan
echo [1] Dang xoa .git cu...
if exist ".git" (
    rmdir /s /q ".git"
    echo     Da xoa .git cu.
) else (
    echo     Khong co .git cu.
)

REM Khoi tao git moi sach
echo [2] Khoi tao git moi...
git init
git branch -M main
git config user.name "Vu Van"
git config user.email "vuvancaoph@gmail.com"

REM Them remote
echo [3] Them remote GitHub...
git remote add origin https://github.com/vuvancaoph-cloud/cbi-quotation-bot.git

REM Add tat ca file
echo [4] Them file vao Git...
git add .
git status

REM Commit
echo [5] Tao commit...
git commit -m "Initial commit: CBI Quotation Bot v1.0"

REM Push
echo.
echo [6] Dang push len GitHub...
echo     (Trinh duyet co the mo ra de xac thuc - hay dang nhap neu duoc yeu cau)
echo.
git push -u origin main --force

echo.
if errorlevel 1 (
    echo [LOI] Push that bai!
    echo Chup man hinh loi nay gui cho tro ly.
) else (
    echo ============================================
    echo   THANH CONG! Kiem tra tai:
    echo   https://github.com/vuvancaoph-cloud/cbi-quotation-bot
    echo ============================================
)
echo.
pause
