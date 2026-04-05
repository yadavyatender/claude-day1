@echo off
REM Gold Rate Tracker - Quick Start Script for Windows

echo.
echo ============================================================
echo   GOLD 22K RATE TRACKER - STARTING APPLICATION
echo ============================================================
echo.
echo Running: python main.py
echo.
echo The application will:
echo  [*] Fetch current gold price
echo  [*] Send email to yatenderyadav489@gmail.com
echo  [*] Continue checking every hour for 24 hours
echo  [*] Switch to weekly checks after 24 hours
echo.
echo To stop: Press Ctrl + C
echo.
echo ============================================================
echo.

python main.py

if errorlevel 1 (
    echo.
    echo ERROR: Application failed to start
    echo.
    echo Troubleshooting:
    echo 1. Make sure you're in the project directory
    echo 2. Check that dependencies are installed: pip install -r requirements.txt
    echo 3. Make sure .env has GMAIL_PASSWORD set
    echo 4. Check gold_tracker.log for error details
    echo.
    pause
    exit /b 1
)
