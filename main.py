import ssl
import uvicorn
from fastapi import FastAPI

from src import logger
from src.middlewares.errors import exception_middleware
from src.middlewares.log import request_log_middleware
from src.modules.classes import handler as class_handler

ssl._create_default_https_context = ssl._create_unverified_context
logger.init_loggers()

app = FastAPI()

# Register Middleware
app.middleware("http")(exception_middleware)
app.middleware("http")(request_log_middleware)

# Include routers
app.include_router(class_handler.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
