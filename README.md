# linux-monitor

Simple Linux system monitoring tool that reads from `/proc`.

## Requirements
- Linux (tested on [Ubuntu Server 24.04](https://ubuntu.com/download/server/thank-you?version=24.04.3&architecture=arm64))
- Python 3

## Run
```bash
python3 monitor.py
```

Monitor should print something like

```yaml
CPU:   23%
MEM:   1.1GB / 3.8GB
DISK:  42% used
SSH:   active
ERRORS (last 5 min): 0
```

## Metrics

- CPU usage (computed from `/proc/stat` deltas)
- Memory usage (`MemTotal` - `MemAvailable` from `/proc/meminfo`)