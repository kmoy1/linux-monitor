#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="linux-monitor"
UNIT_PATH="/etc/systemd/system/${SERVICE_NAME}.service"

sudo systemctl stop "${SERVICE_NAME}" || true
sudo systemctl disable "${SERVICE_NAME}" || true
sudo rm -f "${UNIT_PATH}"
sudo systemctl daemon-reload

echo "Uninstalled ${SERVICE_NAME}."
