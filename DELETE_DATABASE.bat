@echo off
REM Direct database deletion using Windows commands

echo.
echo ============================================================
echo   DELETING DATABASE FILE (gold_rates.db)
echo ============================================================
echo.

cd /d "%~dp0"

REM Check if file exists
if exist "gold_rates.db" (
    echo Found: gold_rates.db
    echo Attempting to delete...
    del /F /Q "gold_rates.db"
    
    if exist "gold_rates.db" (
        echo ✗ FAILED - File is locked by another process
        echo   Please close all Python processes and try again
        echo   Or manually delete: gold_rates.db
    ) else (
        echo ✓ DELETED: gold_rates.db
    )
) else (
    echo ✓ File already deleted or doesn't exist
)

echo.
echo ============================================================
echo   STARTING APPLICATION WITH FRESH DATABASE
echo ============================================================
echo.
echo Next: Run the application
echo Command: python main.py
echo.
pause
