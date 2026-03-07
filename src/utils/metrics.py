from fastapi import Request,Response,FastAPI
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from prometheus_client import Counter,Histogram,generate_latest,CONTENT_TYPE_LATEST
import time

Request_Counetr=Counter("http_requests_total","TOTAL HTTP REQUESTS",["method","endpoint","status"])
Request_Histogram=Histogram("http_requests_duration_seconds","HTTP REQUESTS LATENCY",["method","endpoint"])

class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time=time.time()

        response= await call_next(request)

        duration=time.time()-start_time
        endpoint = request.url.path

        Request_Counetr.labels(method=request.method,endpoint=endpoint,status=response.status_code).inc()
        Request_Histogram.labels(method=request.method,endpoint=endpoint).observe(duration)

        return response
    

def setup_metrics(app: FastAPI):
   
    app.add_middleware(PrometheusMiddleware)

    @app.get("/TrhBVe_m5gg2002_E5VVqS", include_in_schema=False)
    def metrics():
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
        