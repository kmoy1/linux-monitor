# linux-monitor

Simple Linux system monitoring tool that reads from `/proc`.

## Requirements
- Linux (tested on [Ubuntu Server 24.04](https://ubuntu.com/download/server/thank-you?version=24.04.3&architecture=arm64))
- Python 3

### Time Sync Fix (VM)
Alert timestamps may look incorrect. To fix, resync the VM clock (UTC):

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

Alerts print only when a status changes. In a transition state from OK -> CRIT, alert history would display:

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

- CPU usage (computed from `/proc/stat` deltas)
- Memory usage (`MemTotal` - `MemAvailable` from `/proc/meminfo`)