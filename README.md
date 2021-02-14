# Example Grafana, Prometheus Monitoring with URL Shortening Service

## Installation

**One**: Docker, Docker Compose must be installed.:

**Two**: Run this command at the same directory with `stack.yaml`:
```
docker-compose -f stack.yaml up --build
```

## Services

We have three services:

* URL Shortener
* Prometheus
* Grafana

## URL Shortener
There is [FastAPI](https://fastapi.tiangolo.com/) service to shorten urls.

I write a class `CleanAPI` which handles requests and responses with [cleanuri.com](https://cleanuri.com/docs).

```python
class CleanAPI:
    """Class for manage clean api requests."""

    BASE_URL = "https://cleanuri.com/api/v1/shorten"

    def shorten(self, url: str) -> dict:
        """Request to cleanapi to shorten given url.

        Args:
            url (str): URL to short.

        Returns:
            dict: Result dict according to response.
                  If results is OK, returns `status` is True,
                  `url` which is given url and `short_url` which is shortened url.
                  Otherwise returns `status` False and `error` which is error message.
        """        
        try:
            resp = req.post(self.BASE_URL, data={"url": url}).json()

            if resp.get("error", None) is not None:
                result = {"status": False, "error": resp["error"]}
            else:
                result = {"status": True, "short_url": resp["result_url"]}

        except Exception as e:
            result = {"status": False, "error": str(e)}

        return result
```

I used [`prometheus-fastapi-instrumentator`](https://github.com/trallnag/prometheus-fastapi-instrumentator) to send metrics.

Also, I wrote three custom metric for prometheus.

**One**: Mem and Cpu usage metric.
```python
def cpu_mem_usage_metric() -> Callable[[Info], None]:
    METRIC_CPU = Gauge('cpu_usage', 'CPU Usage')
    METRIC_MEM = Gauge('mem_usage', 'MEM Usage')

    def instrumentation(info: Info) -> None:
        METRIC_CPU.set(psutil.cpu_percent())
        METRIC_MEM.set(psutil.virtual_memory().percent)

    return instrumentation
```
**Second**: Status code distribution metric.
```python
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
```
**Three**: Total request count metric.
```python
def request_total_count_metric() -> Callable[[Info], None]:
    METRIC = Counter('request_total_count_metric', 'request_total_count_metric')

    def instrumentation(info: Info) -> None:
        METRIC.inc()

    return instrumentation
```

## Prometheus
This is our `prometheus.yaml` file.
```yaml
global:
  scrape_interval: 30s
  scrape_timeout: 10s

rule_files:
  - alert.yml

scrape_configs:
  - job_name: services
    metrics_path: /metrics
    static_configs:
      - targets:
          - 'prometheus:9090'
          - 'url_shortener:8000'
```
This is `alert.yaml` to alert when services are down.
```yaml
groups:
  - name: DemoAlerts
    rules:
      - alert: InstanceDown 
        expr: up{job="services"} < 1 
        for: 5m 
```
## Grafana
Look at `http://localhost:3000` to see Grafana dashboard.

### Cpu and Mem Usage:
![alt text](https://github.com/madogan/URLShortener/blob/master/cpu_mem_graph.png?raw=true)
### Request Stats:
![alt text](https://github.com/madogan/URLShortener/blob/master/request_stats_graph.png?raw=true)
