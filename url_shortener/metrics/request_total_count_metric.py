from typing import Callable
from prometheus_client import Counter
from prometheus_fastapi_instrumentator.metrics import Info


def request_total_count_metric() -> Callable[[Info], None]:
    METRIC = Counter('request_total_count_metric', 'request_total_count_metric')

    def instrumentation(info: Info) -> None:
        METRIC.inc()

    return instrumentation
