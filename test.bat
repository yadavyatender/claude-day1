@echo off
REM Gold Rate Tracker - Test Setup Script for Windows

echo.
echo ============================================================
echo   GOLD 22K RATE TRACKER - SETUP TEST
echo ============================================================
echo.

python test_setup.py

if errorlevel 1 (
    echo.
    echo ERRORS FOUND - Please fix the issues above
    echo.
    pause
    exit /b 1
) else (
    echo.
    echo All tests passed!
    echo.
    echo Next step: Run the application
    echo Command: python main.py
    echo.
    pause
    exit /b 0
)
