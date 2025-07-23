import logging
import time
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import List
from app.models.task import Task
from app.services.task_service import TaskManager
from app.config.get_logger import get_logger
from app.config.middleware import logging_middleware
from api.task_routes import router as task_router

# Creating our application - like naming our project
app = FastAPI()
app.middleware("http")(logging_middleware)

#logger config
logger = get_logger()
logger.info("Server is starting...")

#task manager instance
task_manager = TaskManager()
	
#mount the router
app.include_router(task_router, prefix="/api")

   



