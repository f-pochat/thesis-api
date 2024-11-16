import ssl
import uvicorn
from fastapi import FastAPI

from src import logger
from src.middlewares.errors import exception_middleware
from src.middlewares.log import request_log_middleware
from src.modules.classes import handler as class_handler
from src.modules.chat import handler as chat_handler
import nltk

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt_tab')

logger.init_loggers()

app = FastAPI()

# Register Middleware
app.middleware("http")(exception_middleware)
app.middleware("http")(request_log_middleware)

# Include routers
app.include_router(class_handler.router)
app.include_router(chat_handler.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
