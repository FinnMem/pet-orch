import time
import random
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram

from app.api import routes  # Основные роуты
from app.core.config import settings  # Централизованная конфигурация

app = FastAPI()

# Метрики Prometheus
Instrumentator().instrument(app).expose(app)

JOBS_DISPATCHED = Counter("petorch_jobs_dispatched_total", "Total jobs dispatched")
JOBS_SUCCESS = Counter("petorch_jobs_success_total", "Total successful jobs")
JOBS_FAILURE = Counter("petorch_jobs_failure_total", "Total failed jobs")
JOB_DURATION = Histogram("petorch_job_duration_seconds", "Job processing duration")

# Подключаем маршруты
app.include_router(routes.router)

@app.get("/health")
def health():
    return {
        "status": "ok",
        "timestamp": time.time(),
        "redis_url": settings.redis_url,
        "db_url": settings.database_url,
    }

@app.post("/run-job")
def run_job():
    JOBS_DISPATCHED.inc()
    start_time = time.time()

    try:
        duration = random.uniform(0.1, 1.5)
        time.sleep(duration)

        if random.random() < 0.8:
            JOBS_SUCCESS.inc()
            return {"status": "success", "duration": duration}
        else:
            raise Exception("Simulated job failure")
    except Exception as e:
        JOBS_FAILURE.inc()
        return {"status": "failure", "error": str(e)}
    finally:
        JOB_DURATION.observe(time.time() - start_time)