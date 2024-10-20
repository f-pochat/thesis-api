from fastapi.responses import JSONResponse

from pydantic import ValidationError
from src.logger import log
from fastapi import Request


async def exception_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except ValidationError as ve:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Invalid input",
                "details": ve.errors()
            }
        )
    except Exception as e:
        log.error(f"An error occurred: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "details": str(e)
            }
        )
