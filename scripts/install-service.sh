#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="linux-monitor"
USER_NAME="${1:-kevinmoy}"
WORKDIR="${2:-/home/kevinmoy/linux-monitor}"
PYTHON_BIN="${3:-/usr/bin/python3}"

UNIT_PATH="/etc/systemd/system/${SERVICE_NAME}.service"

sudo tee "${UNIT_PATH}" >/dev/null <<EOF
[Unit]
Description=Linux Monitor Agent
After=network.target

[Service]
Type=simple
User=${USER_NAME}
WorkingDirectory=${WORKDIR}
ExecStart=${PYTHON_BIN} ${WORKDIR}/monitor.py
Restart=on-failure
RestartSec=2

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable "${SERVICE_NAME}"
sudo systemctl start "${SERVICE_NAME}"

echo "Installed and started ${SERVICE_NAME}. Check status with: systemctl status ${SERVICE_NAME}"
