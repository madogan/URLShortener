import json

from typing import Callable
from prometheus_client import Counter, Histogram
from prometheus_fastapi_instrumentator.metrics import Info


def request_status_code_metric() -> Callable[[Info], None]:
    HISTOGRAM = Histogram('request_status_code_metric',
                          'Distribution of status codes.')

    def instrumentation(info: Info) -> None:
        if info.response:
            HISTOGRAM.observe(info.response.status_code)
        else:
            HISTOGRAM.observe(404)

    return instrumentation
