def fmt_bytes(n):
    """Convert bytes to human readable (e.g. GiB)."""
    units = ["B", "KiB", "MiB", "GiB", "TiB"]
    v = float(n)
    for u in units:
        if v < 1024.0 or u == units[-1]:
            return f"{v:.1f}{u}"
        v /= 1024.0
    return f"{n}B"
