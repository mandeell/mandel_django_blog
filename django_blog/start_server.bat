@echo off
echo Starting Django Blog Server...
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies if needed
echo Checking dependencies...
pip install -r requirements.txt --quiet

REM Run migrations
echo Running database migrations...
venv\Scripts\python.exe manage.py migrate

REM Start the server
echo.
echo Starting development server...
echo Blog will be available at: http://127.0.0.1:8000/
echo Admin panel will be available at: http://127.0.0.1:8000/admin-panel/
echo.
echo Press Ctrl+C to stop the server
echo.

venv\Scripts\python.exe manage.py runserver

pause