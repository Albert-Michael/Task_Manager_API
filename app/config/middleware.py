import time
import logging
from fastapi import Request
from starlette.middleware.base import RequestResponseEndpoint, BaseHTTPMiddleware
from starlette.responses import Response

#  ===== SETTING UP OUR ROUTES + LOGGING =====
async def log_request_info(request: Request, call_next):
    """Log details of every request made to the API"""
    logger = logging.getLogger("uvicorn.access")
    start_time = time.time()

    logger.info(f"Incoming Request: {request.method}, {request.url}")

    body = await request.body()
    try:
        body_text = body.decode("utf-8")
    except UnicodeDecodeError:
        body_text = "<binary data>"

    logger.info(f"Request body: {body_text}")

    response = await call_next(request)
    process_time = round(time.time() - start_time, 4)

    logger.info(f"Response status: {response.status_code}, took {process_time}s")

    return response

def logging_middleware():
    return BaseHTTPMiddleware(dispatch=log_request_info)