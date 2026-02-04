import subprocess
import time
import shutil


def cpu_times_snapshot():
    with open("/proc/stat") as f:
        for line in f:
            if line.startswith("cpu "):
                parts = line.split()
                values = list(map(int, parts[1:]))
                return values
        raise RuntimeError("cpu line not found")


def get_cpu_usage(interval=0.25):
    """Get CPU usage percentage over a short sampling interval."""
    t1 = cpu_times_snapshot()
    time.sleep(interval)
    t2 = cpu_times_snapshot()

    total1 = sum(t1)
    total2 = sum(t2)

    # Idle time = time CPU had nothing runnable (idle + iowait)
    idle1 = t1[3] + t1[4]
    idle2 = t2[3] + t2[4]

    total_delta = total2 - total1
    if total_delta <= 0:
        return 0.0
    idle_delta = idle2 - idle1

    return 100 * (1 - idle_delta / total_delta)


def get_memory_usage():
    """Return (used_kb, total_kb, available_kb) from /proc/meminfo."""
    mem = {}
    with open("/proc/meminfo") as f:
        for line in f:
            k, v = line.split(":")
            mem[k] = int(v.strip().split()[0])
    used = mem["MemTotal"] - mem["MemAvailable"]
    return used, mem["MemTotal"], mem["MemAvailable"]


def get_disk_usage(path="/"):
    """Return (used_bytes, total_bytes, used_pct) for a filesystem."""
    total, used, free = shutil.disk_usage(path)
    used_pct = (used / total) * 100.0 if total else 0.0
    return used, total, used_pct


def get_service_state(service_name="ssh"):
    """Return systemd service state string."""
    p = subprocess.run(
        ["systemctl", "is-active", service_name],
        capture_output=True,
        text=True,
    )
    state = (p.stdout or "").strip()
    if state:
        return state
    return "unknown"


def count_recent_errors(since="5 min ago"):
    """Counts journal entries at priority err (3) or worse since a window."""
    p = subprocess.run(
        ["journalctl", "-p", "err", "--since", since, "--no-pager", "-o", "short-iso"],
        capture_output=True,
        text=True,
    )
    out = (p.stdout or "").strip()
    if not out or out == "-- No entries --":
        return 0

    return sum(1 for line in out.splitlines() if line and line[0].isdigit())
