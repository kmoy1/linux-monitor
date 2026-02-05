# linux-monitor

Simple Linux monitoring agent with thresholds, alerts, and overall OK/WARN/CRIT status.

## Requirements
- Linux (tested on [Ubuntu Server 24.04](https://ubuntu.com/download/server/thank-you?version=24.04.3&architecture=arm64))
- Python 3

### Time Sync Fix (VM)
Alert timestamps are in UTC. If they look wrong, resync the VM clock:

```bash
sudo systemctl restart systemd-timesyncd
sudo timedatectl set-ntp false
sudo timedatectl set-ntp true
timedatectl
```

## Run
```bash
python3 monitor.py
```

In standard non-alert state monitor would display something like:

```yaml
CPU usage:  0.40%
Memory used:  1200MB / 3900MB
Disk used: 8.0GiB / 61.7GiB (13.0%)
SSH service status:  active
Errors (since 5 min ago): 0
OVERALL: OK
```

Alerts print only when a status changes and are kept in history. In a transition state from OK -> CRIT, alert history would display:

```yaml
CPU usage:  1.61%
Memory used:  1220MB / 3900MB
Disk used: 8.0GiB / 61.7GiB (13.0%)
FAKE-SERVICE service status:  inactive
Errors (since 5 min ago): 0
OVERALL: CRIT
ALERTS:
  2026-02-05T07:15:04+00:00 SERVICE: OK -> CRIT
  2026-02-05T07:15:04+00:00 OVERALL: OK -> CRIT
```

## Metrics
- CPU usage (computed from `/proc/stat`)
- Memory usage (`MemTotal` - `MemAvailable` from `/proc/meminfo`)
- Disk usage (percent used, from `shutil.disk_usage`)
- Service state (`systemctl is-active`)
- Recent error count (`journalctl -p err --since ...`)
- Overall status (`OK | WARN | CRIT`)

## Systemd Service (VM)
Install and start:

```bash
bash scripts/install-service.sh
```

Read logs after start:

```bash
journalctl -u linux-monitor -f
```

Stop/disable:

```bash
sudo systemctl stop linux-monitor
sudo systemctl disable linux-monitor
```

Uninstall:

```bash
bash scripts/uninstall-service.sh
```
