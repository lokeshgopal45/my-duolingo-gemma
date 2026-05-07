@echo off
REM Quick setup script for Gemma Validation on Windows

echo.
echo 🚀 Gemma Validation - Quick Setup
echo ==================================

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+ from https://python.org
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do echo ✅ %%i

REM Create venv if needed
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate venv
call venv\Scripts\activate.bat

REM Install dependencies
echo 📚 Installing dependencies...
pip install -q -r requirements.txt

REM Navigate to validation directory
cd gemma_validation

REM Run migrations
echo 🔄 Initializing database...
python manage.py migrate --no-input

REM Load sample data
echo 📝 Loading sample exercises...
python manage.py load_sample_exercises

echo.
echo ✅ Setup complete!
echo.
echo 📖 Next steps:
echo   1. Make sure Ollama/LM Studio is running
echo   2. In another terminal, start the API server:
echo      python run_server.py
echo   3. In another terminal, run tests:
echo      python test_validation.py
echo   4. Access the API:
echo      http://localhost:8000/api/exercises/
echo.
echo For more details, see GETTING_STARTED.md
echo.
pause
