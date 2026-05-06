from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from api.controllers.auth_controller import router as auth_router_async
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="FastAPI CLASS")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Async Request: {request.method} {request.url}")
    response = await call_next(request)
    print(f"Async Response status: {response.status_code}")
    return response

@app.exception_handler(HTTPException)
async def exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail, "status": False},
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)



app.include_router(auth_router_async, prefix="/auth", tags=["Authentication"])
