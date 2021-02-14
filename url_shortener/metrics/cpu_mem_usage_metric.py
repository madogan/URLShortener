import json
import psutil

from typing import Callable
from prometheus_client import Gauge
from prometheus_fastapi_instrumentator.metrics import Info


def cpu_mem_usage_metric() -> Callable[[Info], None]:
    METRIC_CPU = Gauge('cpu_usage', 'CPU Usage')
    METRIC_MEM = Gauge('mem_usage', 'MEM Usage')

    def instrumentation(info: Info) -> None:
        METRIC_CPU.set(psutil.cpu_percent())
        METRIC_MEM.set(psutil.virtual_memory().percent)

    return instrumentation
