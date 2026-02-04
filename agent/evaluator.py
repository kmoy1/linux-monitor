from .status import STATUS_OK, STATUS_WARN, STATUS_CRIT


def evaluate_cpu(cpu_pct, window, thresholds):
    window.add(cpu_pct)
    if window.all_at_or_above(thresholds.crit_pct):
        return STATUS_CRIT
    if window.all_at_or_above(thresholds.warn_pct):
        return STATUS_WARN
    return STATUS_OK


def evaluate_memory(available_mb, thresholds):
    if available_mb < thresholds.crit_available_mb:
        return STATUS_CRIT
    if available_mb < thresholds.warn_available_mb:
        return STATUS_WARN
    return STATUS_OK


def evaluate_disk(used_pct, thresholds):
    if used_pct >= thresholds.crit_used_pct:
        return STATUS_CRIT
    if used_pct >= thresholds.warn_used_pct:
        return STATUS_WARN
    return STATUS_OK


def evaluate_errors(error_count, thresholds):
    if error_count >= thresholds.crit_count:
        return STATUS_CRIT
    if error_count >= thresholds.warn_count:
        return STATUS_WARN
    return STATUS_OK


def evaluate_service(state, thresholds):
    if state != thresholds.required_state:
        return STATUS_CRIT
    return STATUS_OK
