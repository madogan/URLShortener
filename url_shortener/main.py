from typing import Optional
from fastapi import FastAPI
from cleanapi import CleanAPI
from prometheus_fastapi_instrumentator import Instrumentator
from metrics.cpu_mem_usage_metric import cpu_mem_usage_metric
from metrics.request_status_code_metric import request_status_code_metric

# Determine version of the api.
__version__ = "1.0"

# Create app instance.
app = FastAPI()

# Create Clean API instance.
clean_api = CleanAPI()

# Create Prometheus instrumentator instance
# and configure.
instrumentator = Instrumentator()
instrumentator.add(cpu_mem_usage_metric())
instrumentator.add(request_status_code_metric())
instrumentator.instrument(app).expose(app)


@app.post(f"/api/v{__version__}/shorten")
def shorten(url: str) -> dict:
    """Get long URL and shorten it via `cleanapi.com`.

    Args:
        url (str): Long URL to shorten.

    Returns:
        [dict]: Dict result with `status`, `url`, `short_url`
                and `error` if error occurs.
    """
    return {**clean_api.shorten(url)}
