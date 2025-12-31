@echo off
REM OptimusDB Python Client - Windows Setup Script

echo ==================================
echo OptimusDB Python Client Setup
echo ==================================
echo.

REM Check Python
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
echo X Python is required but not found
echo Please install Python 3.8 or higher from python.org
pause
exit /b 1
)

python --version
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
echo X Failed to install dependencies
pause
exit /b 1
)

echo [32mDependencies installed successfully[0m
echo.

REM Test connection
echo Testing connection to OptimusDB...
python optimusdb_client.py health

if errorlevel 1 (
echo.
echo [33mSetup completed but server connection failed[0m
echo Please check if OptimusDB is running and accessible
echo.
echo Try: python optimusdb_client.py health --url http://localhost:8080
echo.
) else (
echo.
echo ==================================
echo [32mSetup completed successfully![0m
echo ==================================
echo.
echo Quick start:
echo   1. Get all documents:     python optimusdb_client.py get
echo   2. Upload TOSCA file:     python optimusdb_client.py upload sample_tosca.yaml
echo   3. Run examples:          python example_usage.py
echo   4. View documentation:    type README.md
echo.
)

pause