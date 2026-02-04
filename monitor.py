# Read /proc/stat
# Sleep X = 250 ms
# Read /proc/stat again 
# Compute deltas to estimate change during time window
# And give overall percentage estimates

import time
import shutil
import subprocess


def cpu_times_snapshot():
    with open("/proc/stat") as f:
        for line in f:
            if line.startswith("cpu "):
                parts = line.split()
                values = list(map(int, parts[1:]))
                return values
        raise RuntimeError("cpu line not found")

# Get CPU usage every <INTERVAL> seconds
def get_cpu_usage(interval=0.25):
    t1 = cpu_times_snapshot()
    time.sleep(interval)
    t2 = cpu_times_snapshot()

    total1 = sum(t1)
    total2 = sum(t2)
    # Use idle time = total time (since boot) 
    # that CPU had nothing runnable (no process needed CPU)
    # t1[3] is idle time = time CPU spent idle
    # t1[4] is iowait time = time CPU idle waiting for I/O
    idle1 = t1[3] + t1[4]
    idle2 = t2[3] + t2[4]
    
    total_delta = total2 - total1
    if total_delta <= 0:
        return 0.0
    idle_delta = idle2 - idle1

    return 100 * (1 - idle_delta / total_delta)

def get_memory_usage():
    mem = {}
    with open("/proc/meminfo") as f:
        for line in f:
            k, v = line.split(":")
            mem[k] = int(v.strip().split()[0])
    used = mem["MemTotal"] - mem["MemAvailable"]
    return used, mem["MemTotal"]

# If disk usage too high, many ops start failing (experienced this IRL with CDK deploy and building pkgs)
def get_disk_usage(path="/"): 
    total, used, free = shutil.disk_usage(path)
    used_pct = (used / total) * 100.0 if total else 0.0 
    return used, total, used_pct

# Check a critical service's (default ssh command) lifecycle state
def get_service_state(service_name="ssh"):
    p = subprocess.run(
        ["systemctl", "is-active", service_name],
        capture_output=True,
        text=True,
    )
    state = (p.stdout or "").strip()
    if state:
        return state
    return "unknown"

# Check if system is logging error events in system journal recently (last 5 mins)
def count_recent_errors(since="5 min ago"):
    """Counts journal entries at priority err (3) or worse since a window."""
    p = subprocess.run(
        ["journalctl", "-p", "err", "--since", since, "--no-pager", "-o", "short-iso"],
        capture_output=True,
        text=True,
    )
    out = (p.stdout or "").strip()
    # Special case is "-- No entries --" which we obv shouldn't count
    if not out or out == "-- No entries --":
        return 0

    return sum(1 for line in out.splitlines() if line and line[0].isdigit())


def fmt_bytes(n):
    # Convert bytes to human readable (e.g. GiB)
    units = ["B", "KiB", "MiB", "GiB", "TiB"]
    v = float(n)
    for u in units:
        if v < 1024.0 or u == units[-1]:
            return f"{v:.1f}{u}"
        v /= 1024.0
    return f"{n}B"


if __name__ == "__main__":
    DISK_WARN_PCT = 90.0 # Warn when disk usage above this threshold
    ERR_WINDOW = "5 min ago"
    SERVICE = "ssh"

    while True:
        print("\033c", end="")  # cls

        cpu = get_cpu_usage()
        used_kb, total_kb = get_memory_usage()
        used_b, total_b, disk_pct = get_disk_usage("/")
        ssh_state = get_service_state(SERVICE)
        err_count = count_recent_errors(ERR_WINDOW)
        
        # Print CPU/memory usage rate in 1s interval
        print(f"CPU:  {cpu:.2f}%")
        print(f"MEM:  {used_kb//1024}MB / {total_kb//1024}MB")

        # Print disk usage in 1s interval (shouldn't change much)
        disk_line = f"DISK: {fmt_bytes(used_b)} / {fmt_bytes(total_b)} ({disk_pct:.1f}%)"
        if disk_pct >= DISK_WARN_PCT:
            disk_line += "  [WARN]"
        print(disk_line)

        # Print service state (default is SSH)
        ssh_line = f"{SERVICE.upper()}:  {ssh_state}"
        if ssh_state != "active":
            ssh_line += "  [ALERT]"
        print(ssh_line)

        # Print errors
        err_line = f"ERRORS (since {ERR_WINDOW}): {err_count}"
        if err_count > 0:
            err_line += "  [ALERT]"
        print(err_line)


        time.sleep(1)

