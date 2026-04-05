@echo off
REM Gold Rate Tracker - Test Email Script

echo.
echo ============================================================
echo   GOLD RATE TRACKER - TEST EMAIL
echo ============================================================
echo.

python test_email.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to send test email!
    echo.
    echo Troubleshooting:
    echo 1. Make sure .env file has GMAIL_PASSWORD set
    echo 2. Use App Password, not regular Gmail password
    echo 3. Enable "Less secure app access" if needed
    echo 4. Check internet connection
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo SUCCESS! Test email sent.
echo ============================================================
echo.
pause
