#!/usr/bin/env bash
# =====================================================================
#  setup-remote.sh - Chuẩn bị SERVER PUBLIC (Ubuntu 22.04/24.04) lần đầu
#  Cách dùng (trên server):  sudo bash setup-remote.sh <deploy_user>
# =====================================================================
set -euo pipefail

DEPLOY_USER="${1:-ubuntu}"
DEPLOY_DIR="/opt/petmanagement"

echo "[1/5] Cài Docker Engine + Docker Compose plugin"
if ! command -v docker >/dev/null 2>&1; then
    curl -fsSL https://get.docker.com | sh
fi
docker --version
docker compose version

echo "[2/5] Cho user '${DEPLOY_USER}' dùng docker không cần sudo"
usermod -aG docker "${DEPLOY_USER}"

echo "[3/5] Tạo thư mục triển khai ${DEPLOY_DIR}"
mkdir -p "${DEPLOY_DIR}"
chown -R "${DEPLOY_USER}:${DEPLOY_USER}" "${DEPLOY_DIR}"

echo "[4/5] Mở firewall (ufw)"
if command -v ufw >/dev/null 2>&1; then
    ufw allow 22/tcp     # SSH
    ufw allow 5000/tcp   # PetManagement App
    ufw allow 3001/tcp   # Grafana
    ufw allow 9091/tcp   # Prometheus
    ufw --force enable
fi

echo "[5/5] Swap 2GB (SQL Server cần >= 2GB RAM)"
if ! swapon --show | grep -q swapfile; then
    fallocate -l 2G /swapfile && chmod 600 /swapfile && mkswap /swapfile && swapon /swapfile
    echo '/swapfile none swap sw 0 0' >> /etc/fstab
fi

echo ""
echo "XONG. Hãy thêm public key của Jenkins vào ~${DEPLOY_USER}/.ssh/authorized_keys"
echo "và mở port 22, 5000, 3001, 9091 trong Security Group của nhà cung cấp cloud."
