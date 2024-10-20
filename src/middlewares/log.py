from src.logger import log
from fastapi import Request


async def request_log_middleware(request: Request, call_next):
    log.info(f"Calling {request.url}")

    # Process the request and get the response
    response = await call_next(request)

    # Optionally log the response status code
    log.info(f"Response status: {response.status_code}")

    return response
