@echo off
chcp 65001 > nul
echo ============================================
echo   Setup Local Git - CBI Quotation Bot
echo ============================================
echo.

cd /d "%~dp0"

REM Xoa .git cu neu bi loi (tao boi sandbox)
if exist ".git" (
    echo Dang xoa .git cu...
    rmdir /s /q ".git" 2>nul
)

REM Khoi tao Git moi
echo Dang khoi tao Git repo...
git init
git branch -m main

REM Cau hinh ten/email
git config user.name "Vu Van"
git config user.email "vuvancaoph@gmail.com"

REM Tao file .env tu template
if not exist ".env" (
    echo Dang tao file .env...
    copy ".env.example" ".env" > nul
    echo [OK] Da tao .env - Nho dien thong tin API vao file nay!
)

REM Commit dau tien
echo Dang tao commit dau tien...
git add .
git commit -m "Initial commit: CBI Quotation Bot project structure"

echo.
echo ============================================
echo   HOAN THANH! Local Git da san sang.
echo ============================================
echo.
echo Cau truc du an:
git log --oneline
echo.
echo Buoc tiep theo:
echo   1. Mo file .env va dien API keys vao
echo   2. Copy CSDL_HangHoa_PA3.xlsx vao thu muc data\
echo   3. Chay: pip install -r requirements.txt
echo   4. Chay: uvicorn main:app --reload
echo.
pause
