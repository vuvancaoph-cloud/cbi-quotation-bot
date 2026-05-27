@echo off
chcp 65001 > nul
echo ============================================
echo   Kiem tra Python tren may tinh
echo ============================================
echo.

echo [1] Thu lenh "python":
python --version 2>nul && echo    =^> Tim thay! || echo    =^> KHONG tim thay

echo.
echo [2] Thu lenh "python3":
python3 --version 2>nul && echo    =^> Tim thay! || echo    =^> KHONG tim thay

echo.
echo [3] Thu lenh "py":
py --version 2>nul && echo    =^> Tim thay! || echo    =^> KHONG tim thay

echo.
echo [4] Tim Python trong thu muc pho bien:
if exist "C:\Python311\python.exe"         echo    =^> C:\Python311\python.exe
if exist "C:\Python312\python.exe"         echo    =^> C:\Python312\python.exe
if exist "C:\Python310\python.exe"         echo    =^> C:\Python310\python.exe
if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" echo    =^> %LOCALAPPDATA%\Programs\Python\Python311\python.exe
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" echo    =^> %LOCALAPPDATA%\Programs\Python\Python312\python.exe
if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" echo    =^> %LOCALAPPDATA%\Programs\Python\Python310\python.exe

echo.
echo [5] PATH hien tai:
echo %PATH%

echo.
pause
