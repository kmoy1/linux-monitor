# linux-monitor

Simple Linux system monitoring tool that reads from `/proc`.

## Requirements
- Linux (tested on [Ubuntu Server 24.04](https://ubuntu.com/download/server/thank-you?version=24.04.3&architecture=arm64))
- Python 3

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
CPU usage:  4.44%
Memory used:  1182MB / 3900MB
Disk used: 8.0GiB / 61.7GiB (13.0%)
BAD-SERVICE service status:  inactive
Errors (since 5 min ago): 0
OVERALL: CRIT
ALERTS:
  2026-02-05T02:30:43 SERVICE: OK -> CRIT
  2026-02-05T02:30:43 OVERALL: OK -> CRIT
```

## Metrics

- CPU usage (computed from `/proc/stat` deltas)
- Memory usage (`MemTotal` - `MemAvailable` from `/proc/meminfo`)