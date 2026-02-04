STATUS_OK = "OK"
STATUS_WARN = "WARN"
STATUS_CRIT = "CRIT"

STATUS_ORDER = {
    STATUS_OK: 0,
    STATUS_WARN: 1,
    STATUS_CRIT: 2,
}


def max_status(statuses):
    """Return the highest severity status from an iterable of statuses."""
    best = STATUS_OK
    for status in statuses:
        if STATUS_ORDER[status] > STATUS_ORDER[best]:
            best = status
    return best
