from typing import Callable
from prometheus_client import Counter
from prometheus_fastapi_instrumentator.metrics import Info


def request_status_code_metric() -> Callable[[Info], None]:
    metrics = {
        200: Counter('requsts_status_code_200', 'Distribution of status code 200'),
        400: Counter('requsts_status_code_400', 'Distribution of status code 400'),
        404: Counter('requsts_status_code_404', 'Distribution of status code 404'),
        405: Counter('requsts_status_code_405', 'Distribution of status code 405'),
    }
    
    def instrumentation(info: Info) -> None:
        if info.response:
            metrics[info.response.status_code].inc()
        else:
            metrics[404].inc()

    return instrumentation
