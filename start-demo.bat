@echo off

echo ================================
echo      CoreERP Demo
echo ================================
echo.

docker compose -f docker-compose.prod.yml up --build -d

echo.
echo ================================
echo Abrindo Cloudflare Tunnel...
echo ================================
echo.

cloudflared tunnel --url http://localhost:5173

pause