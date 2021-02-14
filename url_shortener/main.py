from typing import Optional
from cleanapi import CleanAPI
from fastapi import FastAPI, Response, status
from prometheus_fastapi_instrumentator import Instrumentator
from metrics.cpu_mem_usage_metric import cpu_mem_usage_metric
from metrics.request_total_count_metric import request_total_count_metric
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
instrumentator.add(request_total_count_metric())
instrumentator.instrument(app).expose(app)


@app.post(f"/api/v{__version__}/shorten")
def shorten(url: str, response: Response) -> dict:
    """Get long URL and shorten it via `cleanapi.com`.

    Args:
        url (str): Long URL to shorten.

    Returns:
        [dict]: Dict result with `status`, `url`, `short_url`
                and `error` if error occurs.
    """
    result = clean_api.shorten(url)
    
    if result["status"] == True:
        response.status_code = status.HTTP_200_OK
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
    
    return result
