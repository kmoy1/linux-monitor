# Read /proc/stat
# Sleep X = 250 ms
# Read /proc/stat again 
# Compute deltas to estimate change during time window
# And give overall percentage estimates

import time

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

if __name__ == "__main__":
    while True:
        print("\033c", end="")  # clear screen
        print(f"CPU: {get_cpu_usage():.2f}%")
        used, total = get_memory_usage()
        print(f"MEM: {used//1024}MB / {total//1024}MB")
        time.sleep(1)

