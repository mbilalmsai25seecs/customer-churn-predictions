import os
import sys
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from fastapi.middleware.cors import CORSMiddleware
from app.apis.churn_api import churn_router

def get_application():

    app = FastAPI(title="Customer Churn Predictions API's")
    app.include_router(churn_router, prefix="/api")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app

app = get_application()