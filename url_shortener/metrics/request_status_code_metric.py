import json

from typing import Callable
from prometheus_client import Gauge
from prometheus_fastapi_instrumentator.metrics import Info


def request_status_code_metric() -> Callable[[Info], None]:
    METRIC = Gauge('request_status_code_metric', 'Distribution of status codes.')

    def instrumentation(info: Info) -> None:
        if info.response:
            METRIC.set(info.response.status_code)
        else:
            METRIC.set(404)

    return instrumentation
