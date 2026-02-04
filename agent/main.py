import time

from .collectors import (
    count_recent_errors,
    get_cpu_usage,
    get_disk_usage,
    get_memory_usage,
    get_service_state,
)
from .evaluator import (
    evaluate_cpu,
    evaluate_disk,
    evaluate_errors,
    evaluate_memory,
    evaluate_service,
)
from .state import RollingWindow
from .status import STATUS_OK, max_status
from .thresholds import Thresholds
from .utils import fmt_bytes


class StatusTracker:
    def __init__(self, name, initial=STATUS_OK):
        self.name = name
        self.last = initial

    def update(self, current):
        if current != self.last:
            prev = self.last
            self.last = current
            return prev, current
        return None


def run_loop():
    ERR_WINDOW = "5 min ago"
    SERVICE = "ssh"
    thresholds = Thresholds()
    cpu_window = RollingWindow(thresholds.cpu.consecutive_samples)

    trackers = {
        "cpu": StatusTracker("CPU"),
        "memory": StatusTracker("MEM"),
        "disk": StatusTracker("DISK"),
        "service": StatusTracker("SERVICE"),
        "errors": StatusTracker("ERRORS"),
        "overall": StatusTracker("OVERALL"),
    }

    while True:
        print("\033c", end="")  # cls

        cpu = get_cpu_usage()
        used_kb, total_kb, available_kb = get_memory_usage()
        used_b, total_b, disk_pct = get_disk_usage("/")
        ssh_state = get_service_state(SERVICE)
        err_count = count_recent_errors(ERR_WINDOW)

        cpu_status = evaluate_cpu(cpu, cpu_window, thresholds.cpu)
        mem_status = evaluate_memory(available_kb // 1024, thresholds.memory)
        disk_status = evaluate_disk(disk_pct, thresholds.disk)
        service_status = evaluate_service(ssh_state, thresholds.service)
        errors_status = evaluate_errors(err_count, thresholds.errors)
        overall_status = max_status(
            [cpu_status, mem_status, disk_status, service_status, errors_status]
        )

        print(f"CPU usage:  {cpu:.2f}%")
        print(f"Memory used:  {used_kb//1024}MB / {total_kb//1024}MB")

        disk_line = f"Disk used: {fmt_bytes(used_b)} / {fmt_bytes(total_b)} ({disk_pct:.1f}%)"
        print(disk_line)

        ssh_line = f"{SERVICE.upper()} service status:  {ssh_state}"
        print(ssh_line)

        err_line = f"Errors (since {ERR_WINDOW}): {err_count}"
        print(err_line)

        print(f"OVERALL: {overall_status}")

        alerts = []
        for key, current in [
            ("cpu", cpu_status),
            ("memory", mem_status),
            ("disk", disk_status),
            ("service", service_status),
            ("errors", errors_status),
            ("overall", overall_status),
        ]:
            transition = trackers[key].update(current)
            if transition:
                prev, now = transition
                alerts.append(f"{trackers[key].name}: {prev} -> {now}")

        if alerts:
            print("ALERTS:")
            for line in alerts:
                print(f"  {line}")

        time.sleep(1)


if __name__ == "__main__":
    run_loop()
