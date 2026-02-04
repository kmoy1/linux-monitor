import time

from .collectors import (
    count_recent_errors,
    get_cpu_usage,
    get_disk_usage,
    get_memory_usage,
    get_service_state,
)
from .utils import fmt_bytes


def run_loop():
    DISK_WARN_PCT = 90.0  # Warn when disk usage above this threshold
    ERR_WINDOW = "5 min ago"
    SERVICE = "ssh"

    while True:
        print("\033c", end="")  # cls

        cpu = get_cpu_usage()
        used_kb, total_kb = get_memory_usage()
        used_b, total_b, disk_pct = get_disk_usage("/")
        ssh_state = get_service_state(SERVICE)
        err_count = count_recent_errors(ERR_WINDOW)

        print(f"CPU:  {cpu:.2f}%")
        print(f"MEM:  {used_kb//1024}MB / {total_kb//1024}MB")

        disk_line = f"DISK: {fmt_bytes(used_b)} / {fmt_bytes(total_b)} ({disk_pct:.1f}%)"
        if disk_pct >= DISK_WARN_PCT:
            disk_line += "  [WARN]"
        print(disk_line)

        ssh_line = f"{SERVICE.upper()}:  {ssh_state}"
        if ssh_state != "active":
            ssh_line += "  [ALERT]"
        print(ssh_line)

        err_line = f"ERRORS (since {ERR_WINDOW}): {err_count}"
        if err_count > 0:
            err_line += "  [ALERT]"
        print(err_line)

        time.sleep(1)


if __name__ == "__main__":
    run_loop()
