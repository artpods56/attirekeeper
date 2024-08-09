@echo off


echo Starting Docker Compose...
docker-compose up --build -d

echo Waiting for PostgreSQL to start...
:loop
docker exec postgres-database pg_isready >nul 2>&1
if errorlevel 1 (
    echo Waiting for PostgreSQL...
    timeout /nobreak /t 5 >nul
    goto loop
)

echo PostgreSQL database is running.
echo PostgreSQL database running on address:
docker inspect -f "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}" postgres-database

echo Press any key to close...
pause>nul

@echo on
