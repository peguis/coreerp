Write-Host "🚀 Iniciando CoreERP Demo..." -ForegroundColor Green

Write-Host ""
Write-Host "📦 Subindo containers Docker..."

docker compose -f docker-compose.prod.yml up --build -d

Start-Sleep -Seconds 5


Write-Host ""
Write-Host "🗄️ Verificando backend..."

docker logs coreerp_backend --tail 20


Write-Host ""
Write-Host "🌎 Abrindo tunnel Backend..."

Start-Process powershell -ArgumentList "-NoExit", "-Command", "cloudflared tunnel --edge-ip-version 4 --url http://localhost:8000"


Start-Sleep -Seconds 3


Write-Host ""
Write-Host "🌎 Abrindo tunnel Frontend..."

Start-Process powershell -ArgumentList "-NoExit", "-Command", "cloudflared tunnel --edge-ip-version 4 --url http://localhost:5173"


Write-Host ""
Write-Host "✅ CoreERP Demo iniciado!"
Write-Host ""
Write-Host "Aguarde os links do Cloudflare nas novas janelas."