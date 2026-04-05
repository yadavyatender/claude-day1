@echo off
echo.
echo ============================================================
echo   RESETTING DATABASE - Creating Fresh AED Schema
echo ============================================================
echo.
python reset_database.py
echo.
echo ============================================================
echo   Next: Run the application
echo ============================================================
echo.
echo python main.py
echo.
pause
