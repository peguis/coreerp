# start-demo.ps1

Write-Host "🚀 Iniciando CoreERP Demo..." -ForegroundColor Green

Write-Host ""
Write-Host "📦 Subindo containers Docker..."

docker compose -f docker-compose.prod.yml up --build -d

Start-Sleep -Seconds 5


Write-Host ""
Write-Host "🗄️ Status Backend..."

docker logs coreerp_backend --tail 20


Write-Host ""
Write-Host "🌎 Abrindo Tunnel Backend..."

Start-Process powershell -ArgumentList `
"-NoExit", `
"-Command", `
"cloudflared tunnel --edge-ip-version 4 --url http://localhost:8000"


Start-Sleep -Seconds 3


Write-Host ""
Write-Host "🌎 Abrindo Tunnel Frontend..."

Start-Process powershell -ArgumentList `
"-NoExit", `
"-Command", `
"cloudflared tunnel --edge-ip-version 4 --url http://localhost:5173"


Write-Host ""
Write-Host "================================="
Write-Host "✅ CoreERP Demo iniciado!"
Write-Host "================================="
Write-Host ""
Write-Host "Backend:"
Write-Host "http://localhost:8000"
Write-Host ""
Write-Host "Frontend:"
Write-Host "http://localhost:5173"
Write-Host ""
Write-Host "Login Demo:"
Write-Host "admin@demo.com"
Write-Host "Senha:"
Write-Host "demo123"
Write-Host ""
Write-Host "Aguarde os links Cloudflare nas novas janelas."