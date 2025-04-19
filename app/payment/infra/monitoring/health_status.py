from threading import Lock
from typing import ClassVar
from threading import Lock

class HealthStatusMonitor:
    """
    Singleton para monitorar o status de saúde do sistema.
    Possíveis status: "starting", "healthy", "unhealthy".
    Garante acesso thread-safe.
    """
    _instance: ClassVar["HealthStatusMonitor"] = None
    _instance_lock: ClassVar[Lock] = Lock()

    def __init__(self) -> None:
        self._status: str = "starting"
        self._lock: Lock = Lock()

    @classmethod
    def instance(cls) -> "HealthStatusMonitor":
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance

    def set_healthy(self) -> None:
        with self._lock:
            self._status = "healthy"

    def set_unhealthy(self) -> None:
        with self._lock:
            self._status = "unhealthy"

    def get_status(self) -> str:
        with self._lock:
            return self._status
