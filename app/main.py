import logging
import time

#===== Import FastAPI core modules and dependencies =====
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import List

#====== Importing app components: models, services, logger, middleware, routes ======
from app.models.task import Task
from app.services.task_service import TaskManager
from app.config.get_logger import get_logger
from app.config.middleware import logging_middleware
from app.api.task_routes import router as task_router

#====== Database Initialization ======
from app.config.database import Base, engine
from app.models.task_model import TaskDB

# Create database tables based on the defined models
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application instance
app = FastAPI()
app.middleware(logging_middleware)

#logger config
logger = get_logger()
logger.info("Server is starting...")

#mount the router
app.include_router(task_router, prefix="/api")

   



