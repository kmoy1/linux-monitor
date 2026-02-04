from dataclasses import dataclass


@dataclass(frozen=True)
class CpuThresholds:
    warn_pct: float = 85.0
    crit_pct: float = 95.0
    consecutive_samples: int = 3


@dataclass(frozen=True)
class MemoryThresholds:
    warn_available_mb: int = 500
    crit_available_mb: int = 250


@dataclass(frozen=True)
class DiskThresholds:
    warn_used_pct: float = 90.0
    crit_used_pct: float = 95.0


@dataclass(frozen=True)
class ErrorThresholds:
    warn_count: int = 1
    crit_count: int = 5


@dataclass(frozen=True)
class ServiceThresholds:
    required_state: str = "active"


@dataclass(frozen=True)
class Thresholds:
    cpu: CpuThresholds = CpuThresholds()
    memory: MemoryThresholds = MemoryThresholds()
    disk: DiskThresholds = DiskThresholds()
    errors: ErrorThresholds = ErrorThresholds()
    service: ServiceThresholds = ServiceThresholds()
