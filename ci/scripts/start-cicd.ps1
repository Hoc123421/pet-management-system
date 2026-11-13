# start-cicd.ps1 - Khởi động toàn bộ hệ thống trên máy local (Windows + Docker Desktop)
# Dùng:  .\ci\scripts\start-cicd.ps1          (khởi động)
#        .\ci\scripts\start-cicd.ps1 -Stop    (dừng)
param([switch]$Stop)

Set-Location (Resolve-Path "$PSScriptRoot\..\..")

if ($Stop) {
    docker compose -f docker-compose.monitoring.yml down
    docker compose -f docker-compose.yml down
    docker compose -f docker-compose.ci.yml down
    exit 0
}

Write-Host "[1/3] Jenkins + SonarQube" -ForegroundColor Yellow
docker compose -f docker-compose.ci.yml up -d --build

Write-Host "[2/3] Ung dung PetManagement + SQL Server" -ForegroundColor Yellow
docker compose -f docker-compose.yml up -d --build

Write-Host "[3/3] Prometheus + Grafana + Node Exporter + cAdvisor" -ForegroundColor Yellow
docker compose -f docker-compose.monitoring.yml up -d

Write-Host ""
Write-Host "Jenkins    : http://localhost:8090/view/all/  (admin / admin123)" -ForegroundColor Green
Write-Host "SonarQube  : http://localhost:9000/dashboard?id=PetManagement&codeScope=overall  (admin / Admin@123456)" -ForegroundColor Green
Write-Host "App        : http://localhost:5000  (admin@petcare.com / admin123)" -ForegroundColor Green
Write-Host "Swagger    : http://localhost:5000/swagger" -ForegroundColor Green
Write-Host "Grafana    : http://localhost:3001/d/petmanagement-overview/petmanagement-tong-quan-he-thong  (admin / admin123)" -ForegroundColor Green
Write-Host "Prometheus : http://localhost:9091/targets" -ForegroundColor Green
Write-Host "cAdvisor   : http://localhost:8082" -ForegroundColor Green
