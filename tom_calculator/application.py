import logging
from fastapi import FastAPI
from fastapi.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class SessionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, session):
        super().__init__(app)
        self._session = session

    async def dispatch(self, request, call_next):
        response = await call_next(request)
        return response


app = FastAPI()
app.add_middleware(SessionMiddleware, session=None)

@app.get("/")
async def root():
    return {"message": "Hello World"}
